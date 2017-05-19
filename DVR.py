import sys
import socket
import math
import distanceVec_pb2

#Code for reading from file in progress
#if(len(sys.argv) < 4):
#    print("Usage: python DVR.py <router-id> <port-no> <router-config-file>")
#    exit()

#rid = sys.argv[1]
#pno = sys.argv[2]
#rcf = open(sys.argv[3])

#n = int(rcf.readline().strip())
#neighbours = []
#for nbr in range(n-1):
    #read info about neighbours and store in 2d array

#Function for feeding data into protobuf generated class from file
def readInput(vec):
        cfg = input()
        split = cfg.split()
        vec.ID = split[0]
        vec.cost = float(split[1])
        vec.port = int(split[2])

#for sending UDP packets
def sendDV(MESSAGE):
    IP = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for vec in MESSAGE.neighbours:
        PORT = vec.port
        sock.sendto(MESSAGE.SerializeToString(), (IP, PORT))
    #sock.sendto(str(MESSAGE).encode('utf-8'), (IP, PORT))

print("Enter number of neighbours: ")
n = int(input())
print(n)

distanceVec = distanceVec_pb2.Vector()

for i in range(n):
    readInput(distanceVec.neighbours.add())

#sendDV('localhost', 5000, float('inf'))
sendDV(distanceVec)


#print(distanceVec)
#print(distanceVec.SerializeToString())
#print(distanceVec.ParseFromString(b'\n\n\n\x011\x15\x00\x00\x00@\x18\x03')) <- Extract
#print(distanceVec.neighbours[0].port) <- Extract
