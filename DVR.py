import sys
import socket
import math
import threading
import numpy as np
import distanceVec_pb2
from collections import defaultdict as dd

class IO (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def printMat(self):
        global table
        print("TO | [NEXT HOP-COST]")
        for key,val in table.items():
            print(key, ' | ',end='')
            for key1, val1 in val.items():
                print(key1, "-", "%.2f"%val1, '  ',end='')
            print()

    def takeInput(self):
        global table
        task = int(input('Enter 0 to view Reachability Matrix, 1 to change the cost: '))
        if (task == 0):
            self.printMat()
        if (task == 1):
            link = input('Enter the ID of link to change: ')
            through = input('Enter the hop to change: ')
            cost = input('Enter the new cost:')
            table[link][through] = float(cost)

    def run(self):
        while(1):
            self.takeInput()


########################################
#UDP server running on separate thread
########################################
class server (threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.port = PORT
        self.distanceVec = distanceVec_pb2.Vector()
        self.changed = False

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        while 1:
            self.message, self.adr = self.sock.recvfrom(4096)
            self.distanceVec.ParseFromString(self.message)
            if(self.distanceVec != distanceVec):
                self.changed = True
            #print(distanceVec.neighbours[0].port)

########################################
#Class for Bellman Ford algorithm thread
########################################
class bford (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

    def constructDV(self):
        #TODO Figure out other way to access this global variable
        global distanceVec
        self.newDistVec = distanceVec_pb2.Vector()
        self.newDistVec.source = distanceVec.source
        for key,val in table.items():
            min = float(math.inf)
            for key1,val1 in val.items():
                if(val1 < min):
                    min = val1
            vec = self.newDistVec.neighbours.add()
            vec.ID = key
            vec.cost = min
        #If new distance vector != older one then update
        #older and send new one to all neighbours
        if (self.newDistVec != distanceVec):
            distanceVec = self.newDistVec
            sendDV(distanceVec)
            print('###########################')
            print(distanceVec)

    def run(self):
        while 1:
            if (serv.changed):
                serv.changed = False
                self.linkCostChanged = False
                #TODO Check if distance to source is changed here
                minSource = min(table[serv.distanceVec.source].values())
                for vec in serv.distanceVec.neighbours:
                    if (vec.ID != routerID):                                           #TODO [source][source] is not always the shortest path
                        newVal = vec.cost + minSource
                        if not (vec.ID in table and serv.distanceVec.source in table[vec.ID] and table[vec.ID][serv.distanceVec.source] == newVal):
                            table[vec.ID][serv.distanceVec.source] = vec.cost + minSource  #TODO This will fail when there are link changes. Link changes will appear in vec.ID from neighbour to this router
                            linkCostChanged = True
                if (linkCostChanged):
                    self.constructDV()

########################################
#Function for feeding data into protobuf generated class from file
########################################
def readInput(vec):
    temp_str=configFile.readline()
    split = temp_str.split()
    vec.ID = split[0]
    vec.cost = float(split[1])
    neighbourPorts.append(int(split[2]))
    table[vec.ID][vec.ID] = vec.cost

########################################
#Function for sending UDP packets
########################################
def DVSendTimer():
    threading.Timer(2.0, DVSendTimer).start()
    sendDV(distanceVec)

def sendDV(MESSAGE):
    IP = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for port in neighbourPorts:
        sock.sendto(MESSAGE.SerializeToString(), (IP, port))
    sock.close()

#######################################
# MAIN THREAD
#######################################
table = dd(dict)

#Code for reading from file (in progress)
if(len(sys.argv) < 4):
    print("Usage: python DVR.py <router-id> <port-no> <router-config-file>")
    exit()

routerID = sys.argv[1]
port = int(sys.argv[2])
configFile = open(sys.argv[3])
n = int(configFile.readline().strip())

neighbourPorts = []
distanceVec = distanceVec_pb2.Vector()

#Store the inputs in protobuf ds
distanceVec.source = routerID
for i in range(n):
    readInput(distanceVec.neighbours.add())

#Start UDP server thread
serv = server(port)
serv.start()

#Send distance vector to all neighbours every specified amount of seconds
DVSendTimer()
bellman = bford()
bellman.start()

io = IO()
io.start()

print(table)
