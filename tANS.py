import sys
import os
import tanslib

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = os.curdir + '/' + str(sys.argv[1])
data = tanslib.openFileAsByteArray(path)
probabilitiesTable = tanslib.countProbabilities(data)
print("File's size before compression is: " + str(len(data)) + ' bytes')

print("File's size  after compression is: " + str(len(data)) + ' bytes')

