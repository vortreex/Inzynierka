import math
import pickle
headerLenght = 2834

class ReferenceTable(object):
    def __init__(self):
        self.referenceTable = []
        self.columnsLength = []
        self.Probabilities = []
        self.probabilitiesHeader = []
        self.maxVal = 255 + 2 ** 8

    def countProbabilities(self, Data):
        probabilitiesTable = [0] * 256
        for i in Data:
            probabilitiesTable[i] += 1
        for i in range(0, 256):
            probabilitiesTable[i] /= len(Data)

        self.Probabilities = [[a for a in range(0, 256)], probabilitiesTable]

        return bubbleSort(self.Probabilities)

    def createReferenceTable(self):
        valuesUsed = []
        self.probabilitiesHeader = self.Probabilities[0]

        for i in range(0, len(self.probabilitiesHeader)):
            self.columnsLength.append(math.floor(self.Probabilities[1][i] * self.maxVal))
        self.columnsLength[0] += 1

        for rowNo in range(1, round(max(self.columnsLength) + 1)):
            row = []
            for j in range(0, len(self.Probabilities[0])):
                value = round(rowNo / self.Probabilities[1][j])
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


def saveByteArrayAsFile(compressedData, fileName):
    fileName = str(fileName).split('/')[-1] + '.tans'
    f = open(fileName, 'wb')
    f.write(compressedData)
    f.close()
    print("File's size  after compression is: " + str(len(compressedData)) + ' bytes')


def convertBitsToByteArray(bits):
    byteArray = []
    for i in range(0, int(math.ceil(len(bits) / 8))):
        byteArray.append(int(bits[i * 8:(i + 1) * 8], 2))

    return byteArray, len(bits) % 8 # druga wartosc zwracana to liczba bitow w ostatnim bajcie, bo nie zawsze to jest8 i sie kod pieprzy


def convertByteArrayToBits(byteArray, numOfLastBits):
    bits = ''
    for byte in byteArray[:-1]:
        bits += str(bin(byte))[2:].zfill(8)
    bits += str(bin(byteArray[-1]))[2:].zfill(numOfLastBits)
    return bits


def compress(data, tansTab):
    compressedData = ''
    initialState = tansTab.referenceTable[-1][0] ### maxVal

    for symbol in data:
        targetRow = tansTab.columnsLength[tansTab.probabilitiesHeader.index(symbol)]
        state = [initialState, symbol]
        while state[0] > targetRow:
            if state[0] % 2 == 0:
                compressedData += '0'
            elif state[0] % 2 == 1:
                compressedData += '1'
            state[0] >>= 1

        initialState = tansTab.referenceTable[state[0]-1][tansTab.probabilitiesHeader.index(symbol)]
    return compressedData


def addHeader(data, probalTab, numOfLastBits):
    header = list(pickle.dumps(probalTab))
    return bytes(header + [numOfLastBits] + data)


def removeHeader(compressedData):
    compressedData=list(compressedData)
    header = compressedData[:headerLenght]
    data = compressedData[headerLenght+1:]
    probabilitestTable = pickle.loads(bytes(header))
    return probabilitestTable, data, compressedData[headerLenght]

def decompress(comprData, tansTab):
    decompressedData = []

    return decompressedData


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
