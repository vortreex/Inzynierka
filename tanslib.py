import math
import pickle


class ReferenceTable(object):
    def __init__(self):
        self.referenceTable = []
        self.columnsLength = []
        self.probabilitesHeader = []
        self.maxVal = 255 + 2 ** 8

    def createReferenceTable(self, probabilites):
        valuesUsed = []
        self.probabilitesHeader = probabilites[0]

        for i in range(0, len(probabilites[0])):
            self.columnsLength.append(math.floor(probabilites[1][i] * self.maxVal))
        self.columnsLength[0] += 1

        for rowNo in range(1, round(max(self.columnsLength) + 1)):
            row = []
            for j in range(0, len(probabilites[0])):
                value = round(rowNo / probabilites[1][j])
                value = incrementValueTillNotUsed(value, valuesUsed)
                if rowNo <= self.columnsLength[j]:
                    row.append(value)
                    valuesUsed.append(value)
                else:
                    row.append(0)
            self.referenceTable.append(row)
        self.referenceTable = decrement(self.referenceTable, self.maxVal)
        return self


def openFileAsByteArray(filePath):
    f = open(filePath, 'rb')
    byteMap = list(f.read())
    f.close()
    print("File's size before compression is: " + str(len(byteMap)) + ' bytes')
    return byteMap


def convertBitsToByteArray(bits):
    byteArray = []
    for i in range(0, int(math.ceil(len(bits) / 8))):
        byteArray.append(int(bits[i * 8:(i + 1) * 8], 2))
    return byteArray


def saveByteArrayAsFile(compressedData, fileName):
    newName = str(fileName).split('/')[-1] + '.tans'
    f = open(newName, 'wb')
    f.write(compressedData)
    f.close()
    print("File's size  after compression is: " + str(len(compressedData)) + ' bytes')


def countProbabilities(Data):
    probabilitesTable = [0]*256
    for i in Data:
        probabilitesTable[i] += 1
    for i in range(0, 256):
        probabilitesTable[i] /= len(Data)

    probabilitesTable = [[a for a in range(0, 256)], probabilitesTable]
    probabilitesTable = bubbleSort(probabilitesTable)

    return probabilitesTable


def compress(data, tansTab):
    compressedData = ''
    initialState = tansTab.referenceTable[-1][0] ### maxVal

    for symbol in data:
        targetRow = tansTab.columnsLength[tansTab.probabilitesHeader.index(symbol)]
        state = [initialState, symbol]
        while state[0] > targetRow:
            if state[0] % 2 == 0:
                compressedData += '0'
            elif state[0] % 2 == 1:
                compressedData += '1'
            state[0] >>= 1

        initialState = tansTab.referenceTable[state[0]-1][tansTab.probabilitesHeader.index(symbol)]
    return compressedData


def addHeader(data, probalTab):
    header = list(pickle.dumps(probalTab))
    separator = [255]*4
    return bytes(header + separator + data)

def removeHeader(data):
    pass


def decompress(comprData,tansTab):
    pass


def incrementValueTillNotUsed(val, usedValues):
    #TODO do przeróbki zmienić żeby wartości trochę oscylowały?
    #TODO Albo po prostu będę dekrementował każdy element aż będzie maxVal dobre :p
    if val in usedValues:
        val += 1
        val = incrementValueTillNotUsed(val, usedValues)
    return val


def decrement(tab, maxVal):
    while tab[-1][0] > maxVal:
        for j in range(0, len(tab)):
            for i in range(0, len(tab[0])):
                tab[j][i] -= 1
    return tab


def bubbleSort(tab2D):
    for i in range(len(tab2D[0]) - 1, 0, -1):
        for j in range(i):
            if tab2D[1][j] < tab2D[1][j + 1]:
                tab2D[1][j], tab2D[1][j + 1] = tab2D[1][j + 1], tab2D[1][j]
                tab2D[0][j], tab2D[0][j + 1] = tab2D[0][j + 1], tab2D[0][j]

    return tab2D
