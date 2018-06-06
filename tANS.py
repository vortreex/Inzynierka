import sys
import os
import OpenFile

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = os.curdir + '/' + str(sys.argv[1])
f = OpenFile.openFileAsByteArray(path)

print("File's size before compression is: " + str(len(f)) + ' bytes')

