import sys
import tanslib

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = tanslib.openFileAsByteArray(path)
probabilitiesTable = tanslib.countProbabilities(data)
tansTable = tanslib.ReferenceTable().createReferenceTable(probabilitiesTable)
compressedData = tanslib.compress(data, tansTable)
compressedData = tanslib.convertBitsToByteArray(compressedData)
tanslib.saveByteArrayAsFile(compressedData, sys.argv[1])

