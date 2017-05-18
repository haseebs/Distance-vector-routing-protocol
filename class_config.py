import os
import sys

class DV:
    struct_string=""
    def __init__(self):
        self.ID = 'nil'
        self.cost = 0
        self.port = 0
        self.tot_neighbors=0

    def Config_Input(self):
        self.tot_neighbors=int(input("Enter total number of neighbors: "))
        self.struct_string = (str(self.tot_neighbors) + "\n")
        while(self.tot_neighbors>0):
            self.ID=input("Input neighbor ID:")
            self.cost=input("Input cost: ")
            self.port=input("Input Port: ")
            self.struct_string+=(self.ID+" "+self.cost+" "+self.port+"\n")
            self.tot_neighbors=self.tot_neighbors-1

    def Display(self):
        print(self.struct_string)



newObj=DV()
newObj.Config_Input()
newObj.Display()



