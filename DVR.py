import sys
import socket
import math
import threading
import numpy as np
import distanceVec_pb2
from collections import defaultdict as dd

#UDP server running on separate thread
class server (threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.port = PORT
        self.changed = False
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        while 1:
            self.message, self.adr = self.sock.recvfrom(4096)
            distanceVec.ParseFromString(self.message)
            if(self.message != distanceVec):
                self.changed = True
            #print(distanceVec.neighbours[0].port)

#Function for feeding data into protobuf generated class from file
def readInput(vec):
        cfg = input()
        split = cfg.split()
        vec.ID = split[0]
        vec.cost = float(split[1])
        vec.port = int(split[2])
        table[vec.ID][vec.ID] = vec.cost
        table[routerID][routerID] = 0

#Function for sending UDP packets
def sendDV(MESSAGE):
    IP = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for vec in MESSAGE.neighbours:
        if (vec.port == -1):
            continue
        PORT = vec.port
        sock.sendto(MESSAGE.SerializeToString(), (IP, PORT))
    sock.close()

#################################
# MAIN THREAD
#################################

table = dd(dict)

#Code for reading from file (in progress)
if(len(sys.argv) < 4):
    print("Usage: python DVR.py <router-id> <port-no> <router-config-file>")
    exit()

routerID = sys.argv[1]
port = int(sys.argv[2])
#configFile = open(sys.argv[3])
#n = int(configFile.readline().strip())

print("Enter number of neighbours: ")
n = int(input())

distanceVec = distanceVec_pb2.Vector()

#Store the inputs in protobuf ds
for i in range(n):
    readInput(distanceVec.neighbours.add())

#Start UDP server thread
serv = server(port)
serv.start()

#Send distance vector to all neighbours
sendDV(distanceVec)
print(table)

#print(distanceVec)
#print(distanceVec.SerializeToString())
#print(distanceVec.ParseFromString(b'\n\n\n\x011\x15\x00\x00\x00@\x18\x03')) <- Extract
#print(distanceVec.neighbours[0].port) <- Extract
