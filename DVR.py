import sys
import time
import socket
import math
import threading
import numpy as np
import distanceVec_pb2
from collections import defaultdict as dd

#TODO FIX THE CASE WHERE ALL NEIGHBOURS OF NODE GO DOWN AND IT DOESNT PRINT OUTPUT
#Global constants
MAX_NETWORK_SIZE = 16
TIMEOUT_PERIOD = 15

##################################
#Thread for spotting dead routers
##################################
class TimeOut (threading.Thread):
    #Timers stores the timers
    #isActive is used to set router status
    #down is used to prevent reassignments when the router is already down
    def __init__(self):
        threading.Thread.__init__(self)
        self.Timers = {}
        self.isActive = {}
        self.down = {}

    #Set the values of router that is down to infinity
    def SetRouterDown(self, ID):
        global MAX_NETWORK_SIZE
        global table
        print()
        print(ID, 'HAS TIMED OUT')
        for id, val in table.items():
            if (ID in table[id]):
                table[id][ID] = MAX_NETWORK_SIZE
        bellman.linkCostChanged = True

    def run(self):
        global TIMEOUT_PERIOD
        while(1):
            for ID, timer in self.Timers.items():
                if(self.isActive[ID] == True):
                    self.Timers[ID] = time.time()
                    self.isActive[ID] = False
                    self.down[ID] = False
                elif(self.down[ID] == False and time.time() - timer >= TIMEOUT_PERIOD and self.isActive[ID] == False):
                    self.Timers[ID] = time.time()
                    self.down[ID] = True
                    self.SetRouterDown(ID)


#####################################
#Thread for handling user input and print output
#####################################
class IO (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    #Output reachability matrix
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
        global bellman
        task = int(input('Enter 0 to view Reachability Matrix, 1 to change the cost: '))
        if (task == 0):
            self.printMat()
        if (task == 1):
            link = input('Enter the ID of link to change: ')
            through = input('Enter the hop to change: ')
            cost = input('Enter the new cost:')
            table[link][through] = float(cost)
            #triggered update
            bellman.linkCostChanged = True

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
        global timeOut
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        while 1:
            self.message, self.adr = self.sock.recvfrom(4096)
            self.distanceVec.ParseFromString(self.message)
            if(self.distanceVec != distanceVec):
                self.changed = True
            #When this node was down but has now been restarted
            #if(timeOut.down[self.distanceVec.source]):
            #    flushValues(self.distanceVec.source)
            timeOut.isActive[self.distanceVec.source] = True

########################################
#Class for Bellman Ford algorithm thread
########################################
class bford (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.linkCostChanged = False

    def printRoutes(self):
        global distanceVec
        global MAX_NETWORK_SIZE
        print()
        print("#########################################")
        print("I am Router ", distanceVec.source)
        for vec in distanceVec.neighbours:
            if(vec.cost < MAX_NETWORK_SIZE):
                print("Least cost to", vec.ID, "is", "%.2f"%vec.cost, "through", nextHop[vec.ID])
            else:
                print(vec.ID, "is unreachable")

    #def compare(self):
    #    sizeNew = len(self.newDistVec.neighbours)
    #    sizeOld = len(distanceVec.neighbours)
    #    if (sizeNew != sizeOld):
    #        return True
    #    for i in range(sizeNew):
    #        similar = False
    #        for j in range(sizeNew):
    #            if (distanceVec.neighbours[i].ID == self.newDistVec.neighbours[j].ID):
    #                if(distanceVec.neighbours[i].cost == self.newDistVec.neighbours[j].cost):
    #                    similar = True
    #                    break
    #        if not (similar):
    #            return True
    #    return False

    def constructDV(self):
        #TODO Figure out other way to access this global variable
        global distanceVec
        self.newDistVec = distanceVec_pb2.Vector()
        self.newDistVec.source = distanceVec.source
        for key,val in table.items():
            min = float(math.inf)
            minHop = ''
            for key1,val1 in val.items():
                if(val1 < min):
                    min = val1
                    minHop = key1
            vec = self.newDistVec.neighbours.add()
            vec.ID = key
            vec.cost = min
            nextHop[key] = minHop
        #If new distance vector != older one then update
        #older and send new one to all neighbours
        if (self.newDistVec.neighbours != distanceVec.neighbours):
            distanceVec = self.newDistVec
            sendDV(distanceVec)
            self.printRoutes()

    def run(self):
        global MAX_NETWORK_SIZE
        while 1:
            if (serv.changed):
                serv.changed = False
                #sourceCost = min(table[serv.distanceVec.source].values())
                for vec in serv.distanceVec.neighbours:
                    sourceCost = table[serv.distanceVec.source][serv.distanceVec.source]
                    #If direct link cost is changed by neighbour or router has been restarted
                    if (vec.ID == routerID and table[serv.distanceVec.source][serv.distanceVec.source] >= 16):
                        if (vec.cost != table[serv.distanceVec.source][serv.distanceVec.source]):
                            table[serv.distanceVec.source][serv.distanceVec.source] = vec.cost
                            self.linkCostChanged = True
                    elif (vec.ID != routerID):
                        #When a router is unreachable, eliminate count to infinity
                        if (vec.cost >= MAX_NETWORK_SIZE):
                            newVal = MAX_NETWORK_SIZE
                        #When a dead router is back online
                        elif (sourceCost >= 16 and vec.cost < 16):
                            for vec1 in serv.distanceVec.neighbours:
                                if(vec1.ID == routerID):
                                    sourceCost = vec1.cost
                            table[serv.distanceVec.source][serv.distanceVec.source] = sourceCost
                            newVal = sourceCost + vec.cost
                        #Normal convergence
                        else:
                            newVal = vec.cost + sourceCost
                        if not (vec.ID in table and serv.distanceVec.source in table[vec.ID] and table[vec.ID][serv.distanceVec.source] == newVal):
                            table[vec.ID][serv.distanceVec.source] = newVal
                            self.linkCostChanged = True
            if (self.linkCostChanged):
                self.linkCostChanged = False
                self.constructDV()

########################################
#Function for feeding data into protobuf generated class from file
########################################
def readInput(vec):
    global timeOut
    temp_str=configFile.readline()
    split = temp_str.split()
    vec.ID = split[0]
    vec.cost = float(split[1])
    neighbourPorts[vec.ID] = int(split[2])
    nextHop[vec.ID] = vec.ID
    table[vec.ID][vec.ID] = vec.cost
    timeOut.Timers[vec.ID] = time.time()
    timeOut.isActive[vec.ID] = False
    timeOut.down[vec.ID] = False

########################################
#Functions for sending UDP packets
########################################
def DVSendTimer():
    threading.Timer(2.0, DVSendTimer).start()
    sendDV(distanceVec)

def sendDV(MESSAGE):
    global MAX_NETWORK_SIZE
    IP = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msgBackup = distanceVec_pb2.Vector()
    msgBackup.CopyFrom(MESSAGE)
    #Implementation of poison reverse
    for neighbour, port in neighbourPorts.items():
        for vec in MESSAGE.neighbours:
            #First condition is direct route, no harm if it gets passed through
            #It has to pass through to handle router restarts properly
            if(nextHop[vec.ID] != vec.ID and nextHop[vec.ID] == neighbour):
                vec.cost = MAX_NETWORK_SIZE
        sock.sendto(MESSAGE.SerializeToString(), (IP, port))
        MESSAGE.CopyFrom(msgBackup)
    sock.close()

#def flushValues(ID):
#    global table
#    newTable = dd(dict)
#    for i, j  in table.items():
#        for k, l in j.items():
#            if not ((i == ID) ^ (k == ID)):
#                newTable[i][k] = table[i][k]
#    table = newTable
#    print(ID)
#    print(newTable)
#    io.printMat()

#######################################
# MAIN THREAD
#######################################
table = dd(dict)

#Code for reading from file (in progress)
if(len(sys.argv) < 4):
    print("Usage: python DVR.py <router-id> <port-no> <router-config-file>")
    exit()

#Set initial vars
routerID = sys.argv[1]
port = int(sys.argv[2])
configFile = open(sys.argv[3])
n = int(configFile.readline().strip())

#Initialize dictionaries and DV
nextHop = {}
neighbourPorts = {}
distanceVec = distanceVec_pb2.Vector()

#Initialize TimeOut but dont start it before starting server
timeOut = TimeOut()

#Store the inputs in protobuf ds
distanceVec.source = routerID
for i in range(n):
    readInput(distanceVec.neighbours.add())

#Start UDP server thread
serv = server(port)
serv.start()
timeOut.start()

#Send distance vector to all neighbours every specified amount of seconds
DVSendTimer()
bellman = bford()
bellman.start()

#Start IO thread
io = IO()
io.start()
