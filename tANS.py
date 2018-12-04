import sys
from tanslib import *
import random

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = openFileAsByteArray(path)
CompressionEngine = TabledANS()
probabilitiesTable = CompressionEngine.countProbabilities(data)
CompressionEngine.Probabilities = [[1, 2, 3], [0.45, 0.35, 0.2]]
# data = [0, 156, 57, 38, 34, 114, 1, 7, 148, 221, 141, 231, 106, 92, 80, 117, 246, 255]#, 212, 67, 7, 98, 255, 216]
data = [3, 1, 2, 1, 2, 2, 1, 3, 1, 1]
random.shuffle(data)
# data = [a for a in range(10)]
# CompressionEngine.createReferenceTable()
CompressionEngine.maxVal = 31
CompressionEngine.columnsLength = [14, 10, 6]
CompressionEngine.precisionBits = 5
CompressionEngine.referenceTable = [[2, 3, 5], [4, 6, 10], [7, 8, 15], [9, 11, 20], [12, 14, 25], [13, 17, 30],
                                    [16, 21, None], [18, 22, None], [19, 26, None], [23, 28, None],
                                    [24, None, None], [27, None, None], [29, None, None], [31, None, None]]
compressedData = CompressionEngine.compress(data)

print(compressedData)

# compressedData, numOfBits = convertBitsToByteArray(compressedData)
# compressedData = CompressionEngine.addHeader(compressedData, numOfBits)
#
# saveByteArrayAsFile(compressedData, sys.argv[1])
#
# compressedData, lastBitsnumb = CompressionEngine.removeHeader(compressedData)
#
# compressedData = convertByteArrayToBits(compressedData, lastBitsnumb)
decompressedData = CompressionEngine.decompress(compressedData)
#
# print(decompressedData)
print(decompressedData, decompressedData == data)
