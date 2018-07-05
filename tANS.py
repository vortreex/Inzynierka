import sys
import tanslib

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = tanslib.openFileAsByteArray(path)
probabilitiesTable = tanslib.countProbabilities(data)
print("File's size before compression is: " + str(len(data)) + ' bytes')

tansTab = tanslib.createReferenceTable(probabilitiesTable)

print("File's size  after compression is: " + str(len(data)) + ' bytes')

