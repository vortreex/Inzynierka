import math

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

    columnsLength = []
    valuesUsed = []
    maxVal = 2**(8 + 4)-1
    probabilites=sorted(probabilites, reverse=True)

    for i in range(0, len(probabilites)):
        columnsLength.append(math.floor(probabilites[i]*maxVal))

    referenceTable = [[None for _ in range(256)] for _ in range(max(columnsLength))]
    for columnNumber in range(0, len(columnsLength)):
        for rowNumber in range(0, max(columnsLength)):
            if rowNumber+1 <= columnsLength[columnNumber]:
                value = round((rowNumber+1)/probabilites[columnNumber])
                value = incrementValueTillNotUsed(value, valuesUsed)
                valuesUsed.append(value)
            else:
                value = None

            referenceTable[rowNumber][columnNumber] = value

    referenceTable.append([maxVal]+[None]*255)  # Additional row with valMax
    print(referenceTable)
    print(len(valuesUsed)-len(set(valuesUsed)))
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
        val += 1
        # TODO: Poprawic rekurencje bo za duzo zagniezdzenia// zamienic na while'a
        val = incrementValueTillNotUsed(val, usedValues)
    return val
