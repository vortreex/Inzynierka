import math
import pickle
from loger import logger

headerLenght = 2834
# headerLenght = 51


class TabledANS(object):
    def __init__(self):
        self.referenceTable = []
        self.columnsLength = []
        self.Probabilities = []
        self.precisionBits = 10
        self.maxVal = 2 ** self.precisionBits - 1

    def countProbabilities(self, data):
        probabilitiesTable = [0] * 256
        for i in data:
            probabilitiesTable[i] += 1
        for i in range(256):
            probabilitiesTable[i] /= len(data)

        self.Probabilities = bubbleSort([[a for a in range(256)], probabilitiesTable])
        self.Probabilities = bubbleSort(self.Probabilities)
        return zeroRemover(self.Probabilities)

    def createReferenceTable(self):
        valuesUsed = []

        for i in range(len(self.Probabilities[1])):
            col = math.floor(self.Probabilities[1][i] * self.maxVal)
            if col < 1:
                col = 1
            self.columnsLength.append(col)

        self.columnsLength[0] += 1
        value = self.maxVal - sum(self.columnsLength) + 1
        self.referenceTable = [[None] * len(self.Probabilities[1]) for i in range(self.columnsLength[0])]
        for row in range(self.columnsLength[0]):
            for column in range(len(self.Probabilities[1])):
                if row + 1 <= self.columnsLength[column]:
                    value = incrementValueTillNotUsed(value, valuesUsed)
                    valuesUsed.append(value)
                    self.referenceTable[row][column] = value
                else:
                    break
        self.referenceTable = decrement(self.referenceTable)

    def compress(self, data):
        compressedData = ''
        initialState = self.maxVal

        for symbol in data:
            targetRow = self.columnsLength[self.Probabilities[0].index(symbol)]
            state = [initialState, symbol]
            outputSequence = state[0]
            numberOfOutputBits = 0
            while state[0] > targetRow:
                state[0] >>= 1
                numberOfOutputBits += 1
                # print(outputSequence)
            if numberOfOutputBits != 0:
                    compressedData += bin(outputSequence)[-numberOfOutputBits:]
            # print(compressedData)
            initialState = self.referenceTable[state[0] - 1][self.Probabilities[0].index(symbol)]
        return compressedData + bin(initialState)[2:].zfill(self.precisionBits)

    def decompress(self, comprDat):
        decompressedData = []
        data = int(comprDat[-self.precisionBits:], 2)
        comprDat = comprDat[:-self.precisionBits]
        state = self.findValueInReferenceTable(data)
        decompressedData.append(state[0])

        while comprDat:
            number = bin(state[1]+1)[2:]
            bits = self.precisionBits - len(number)
            data = int(number + comprDat[-bits:], 2)
            comprDat = comprDat[:-bits]
            state = self.findValueInReferenceTable(data)
            decompressedData.append(state[0])

        return decompressedData[::-1][1:]

    def findValueInReferenceTable(self, value):
        state = [0, 0]
        rowNum = 0
        for row in self.referenceTable:
            try:
                column = row.index(value)
                state = [self.Probabilities[0][column], rowNum]
                break
            except ValueError:
                pass
            finally:
                rowNum += 1
        return state

    def addHeader(self, data, numOfLastBits):
        header = list(pickle.dumps(self.Probabilities))
        return bytes(header + [numOfLastBits] + data)

    def removeHeader(self, compressedData):
        compressedData = list(compressedData)
        header = compressedData[:headerLenght]
        data = compressedData[headerLenght + 1:]
        self.Probabilities = pickle.loads(bytes(header))
        return data, compressedData[headerLenght]


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

    return byteArray, len(
        bits) % 8  # druga wartosc zwracana to liczba bitow w ostatnim bajcie, bo nie zawsze to jest8 i sie kod pieprzy


def convertByteArrayToBits(byteArray, numOfLastBits):
    bits = ''
    for byte in byteArray[:-1]:
        bits += str(bin(byte))[2:].zfill(8)
    bits += str(bin(byteArray[-1]))[2:].zfill(numOfLastBits)
    return bits


def incrementValueTillNotUsed(val, usedValues):
    # TODO do przeróbki zmienić żeby wartości trochę oscylowały?
    # TODO Albo po prostu będę dekrementował każdy element aż będzie maxVal dobre :p
    while val in usedValues:
        val += 1
    return val


def decrement(tab):
    const = 0
    for column in range(len(tab[0])):
        for row in range(len(tab)):
            try:
                tab[row][column] -= const
            except TypeError:
                break
    return tab


def bubbleSort(tab2D):
    for i in range(len(tab2D[0]) - 1, 0, -1):
        for j in range(i):
            if tab2D[1][j] < tab2D[1][j + 1]:
                tab2D[1][j], tab2D[1][j + 1] = tab2D[1][j + 1], tab2D[1][j]
                tab2D[0][j], tab2D[0][j + 1] = tab2D[0][j + 1], tab2D[0][j]

    return tab2D


def countEntropy(tab):
    entropy = []
    for i in tab:
        try:
            entropy.append(math.log2(i) * i * -1)
        except ValueError:
            entropy.append(0)
    return sum(entropy)


def zeroRemover(tab2d):
    while 0 in tab2d[1]:
        for index, value in enumerate(tab2d[1]):
            if value == 0:
                del tab2d[0][index]
                del tab2d[1][index]
                break
    return tab2d