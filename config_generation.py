import os
import sys
import re
import glob

def Open():
    #Counter for total number of files
    txtCounter = len(glob.glob1("C:\\Users\\HP\\PycharmProjects\\DVR.py", "*.txt"))
    print("Total number of configration files : ",txtCounter)
    print("\n")

    files = glob.glob('C:\\Users\\HP\\PycharmProjects\\DVR.py\\*.txt')
    # iterate over the list getting each file
    for fle in files:
        # Reading the files after opening
        with open(fle) as f:
            text = f.read()
            print(text,'\n')
            f.close()  # Closing all the files

# Function to edit weights of neighbors in specific file
def Edit_specific():

    filename=input("Enter File Name along with extension: ")
    text_fileA = open(filename, "r+") #Opening text file
    str = text_fileA.readline()  # to skip first line

    text_string=""   #string to store the changed weights inorder to write to file again

    #for loop to edit weights
    for line in text_fileA:

        tempstr = " "  #temporary string to store the replaced substring
        print("Enter new weights: ")
        tempstr = input()

        #replacing substring in file
        print(line.replace(line[2:5], tempstr))
        str2=line.replace(line[2:5], tempstr)

        text_string=text_string+str2   #concatenating tbe string in order to write to file

    text_fileA.truncate()
    text_fileA.close()  #closing file after reading

    temp_fileA=open(filename,"w").close()    # deleting all the file content in order to rewrite

    text_fileA=open(filename,"w+")   #opening the file again in write mode

    # writing content back to file
    text_fileA.write(str)
    text_fileA.write(text_string)

    text_fileA.close()   #closing the file after writing again




Open()    #Calling the function to open all files
print("Enter Y to change weights of text files or N to exit:")
ch=input()
if(ch=='Y'):
    Edit_specific()  #calling function to change weights of specific file









