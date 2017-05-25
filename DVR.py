import sys
import socket
import math
import threading
import numpy as np
import distanceVec_pb2
from collections import defaultdict as dd

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

    def run(self):
        while 1:
            if (serv.changed):
                serv.changed = False
                minSource = min(table[serv.distanceVec.source].values())
                for vec in serv.distanceVec.neighbours:
                    if (vec.ID != routerID):                                           #TODO [source][source] is not always the shortest path
                        table[vec.ID][serv.distanceVec.source] = vec.cost + minSource  #TODO This will fail when there are link changes. Link changes will appear in vec.ID from neighbour to this router
                #print(table)

    def constructDV():
        self.newDistVec = distanceVec_pb2.Vector()
        for key,val in table.items():
            min = float(math.inf)
            for key1,val1 in val.items():
                if(val1 < min):
                    min = val1
            print(k, min)

########################################
#Function for feeding data into protobuf generated class from file
########################################
def readInput(vec):
    temp_str=configFile.readline()
    split = temp_str.split()
    vec.ID = split[0]
    vec.cost = float(split[1])
    vec.port = int(split[2])
    print(vec.ID)
    print(vec.cost)
    print(vec.port)
    table[vec.ID][vec.ID] = vec.cost

########################################
#Function for sending UDP packets
########################################
def sendDV(MESSAGE):
    IP = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for vec in MESSAGE.neighbours:
        if (vec.port == -1):
            continue
        PORT = vec.port
        sock.sendto(MESSAGE.SerializeToString(), (IP, PORT))
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

distanceVec = distanceVec_pb2.Vector()

#Store the inputs in protobuf ds
distanceVec.source = routerID
for i in range(n):
    readInput(distanceVec.neighbours.add())

#Start UDP server thread
serv = server(port)
serv.start()

#Send distance vector to all neighbours
sendDV(distanceVec)
bellman = bford()
bellman.start()
print(table)
