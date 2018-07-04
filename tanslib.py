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
    referenceTable = []
    columnsLength = []
    valuesUsed = []
    maxVal = 31#255 + 2**8

    for i in range(0, len(probabilites)):
        columnsLength.append(round(probabilites[i]*maxVal))
    print(columnsLength)

    for rowNo in range(1, round(max(columnsLength)+1)):
        row = []
        for j in range(0, len(probabilites)):
            value = round(rowNo / probabilites[j])
            value = incrementValueTillNotUsed(value, valuesUsed)
            if rowNo <= columnsLength[j]:
                row.append(value)
                valuesUsed.append(value)
            else:
                row.append(None)

        print(row)
        print(len(row)-len(set(row))-row.count(None))
        referenceTable.append(row)
    return referenceTable


def compress(data, tansTab):
    pass


def addHeader(data, probalTab):
    pass


def removeHeader(data):
    pass


def decompress(comprData,tansTab):
    pass

def incrementValueTillNotUsed(val, usedValues):
    if val in usedValues:
        val -= 1
        val = incrementValueTillNotUsed(val, usedValues)
    return val
