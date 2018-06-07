import sys
import os
import tanslib

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')
print("File's size before compression is: " + str(len(Data)) + ' bytes')

Path = os.curdir + '/' + str(sys.argv[1])
Data = tanslib.openFileAsByteArray(Path)
probabilitiesTable = tanslib.countProbabilities(Data)

print("File's size after compression is: " + str(len(Data)) + ' bytes')

