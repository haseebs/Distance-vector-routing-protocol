import sys

if(len(sys.argv) < 4):
    print("Usage: python DVR.py <router-id> <port-no> <router-config-file>")
    exit()

rid = sys.argv[1]
pno = sys.argv[2]
rcf = open(sys.argv[3])

n = int(rcf.readline().strip())
neighbours = []
#for nbr in range(n-1):
    #read info about neighbours and store in 2d array
