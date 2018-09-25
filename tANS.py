import sys
from tanslib import *

print('Compressing file: ' + str(sys.argv[1]) + ' with tANS method')

path = str(sys.argv[1])
data = openFileAsByteArray(path)
CompressionEngine = ReferenceTable()
# probabilitiesTable = CompressionEngine.countProbabilities(data)
CompressionEngine.Probabilities = [[1, 2, 3], [0.45, 0.35, 0.2]]
# data = [0, 156, 57, 38, 34, 114]
data = [1, 2, 1, 3]
CompressionEngine.createReferenceTable()
CompressionEngine.maxVal = 31
CompressionEngine.columnsLength = [14, 10, 6]
CompressionEngine.precisionBits = 5
CompressionEngine.referenceTable = [[2, 3, 5], [4, 6, 10], [7, 8, 15], [9, 11, 20], [12, 14, 25], [13, 17, 30],
                                    [16, 21, None], [18, 22, None], [19, 26, None], [23, 28, None],
                                    [24, None, None], [27, None, None], [29, None, None], [31, None, None]]
compressedData = CompressionEngine.compress(data)
print(data)
print(CompressionEngine.referenceTable)
cprdata1 = compressedData
print(cprdata1)
# print(cprdata1)
# compressedData, numOfBits = convertBitsToByteArray(compressedData)
# cprdata2 = compressedData
# print(cprdata2)
# compressedData = addHeader(compressedData, probabilitiesTable, numOfBits)
# saveByteArrayAsFile(compressedData, sys.argv[1])
# probalTab , comprData2, lastBitsnumb = removeHeader(compressedData)
# comprData1 = convertByteArrayToBits(comprData2, lastBitsnumb)
decompressedData = CompressionEngine.decompress(compressedData)
print(decompressedData)
print(decompressedData == data,)
