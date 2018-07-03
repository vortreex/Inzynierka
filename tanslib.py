def openFileAsByteArray(filePath):
    f = open(filePath, 'rb')
    byteMap = list(f.read())
    f.close()
    return byteMap


def countProbabilities(Data):
    probabilitesTable = [0]*256
    for i in Data:
        probabilitesTable[i] += 1
    for i in range(0, 256):
        probabilitesTable[i] /= len(Data)
    return probabilitesTable

def createReferenceTable(probabilites):
    pass

def compress(data,probalTab):
    pass

def addHeader(data):
    pass

def removeHeader(data):
    pass

def decompress(comprData,probalTab):
    pass

