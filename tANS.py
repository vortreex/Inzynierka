import sys
from tanslib import *

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = openFileAsByteArray(path)
CompressionEngine = ReferenceTable()
probabilitiesTable = CompressionEngine.countProbabilities(data)
tansTable = CompressionEngine.createReferenceTable()
compressedData = compress(data, tansTable)
cprdata1 = compressedData
compressedData, numOfBits = convertBitsToByteArray(compressedData)
cprdata2 = compressedData
compressedData = addHeader(compressedData, probabilitiesTable, numOfBits)
saveByteArrayAsFile(compressedData, sys.argv[1])
probalTab , comprData2, lastBitsnumb = removeHeader(compressedData)
comprData1 = convertByteArrayToBits(comprData2, lastBitsnumb)

