import sys
from tanslib import *

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = openFileAsByteArray(path)
CompressionEngine = TabledANS()
probabilitiesTable = CompressionEngine.countProbabilities(data)
entropy = countEntropy(probabilitiesTable[1])
CompressionEngine.createReferenceTable()
compressedData = CompressionEngine.compress(data)
compressedData, numOfBits = convertBitsToByteArray(compressedData)
compressedData = CompressionEngine.addHeader(compressedData, numOfBits)
saveByteArrayAsFile(compressedData, sys.argv[1])
compressedData, lastBitsnumb = CompressionEngine.removeHeader(compressedData)
compressedData = convertByteArrayToBits(compressedData, lastBitsnumb)
decompressedData = CompressionEngine.decompress(compressedData)
