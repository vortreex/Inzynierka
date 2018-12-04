import math
import pickle
# headerLenght = 2834
headerLenght = 51


class TabledANS(object):
    def __init__(self):
        self.referenceTable = []
        self.columnsLength = []
        self.Probabilities = []
        self.precisionBits = 10
        self.maxVal = 2**self.precisionBits - 1

    def countProbabilities(self, data):
        probabilitiesTable = [0] * 256
        for i in data:
            probabilitiesTable[i] += 1
        for i in range(256):
            probabilitiesTable[i] /= len(data)

        self.Probabilities = bubbleSort([[a for a in range(256)], probabilitiesTable])
        return bubbleSort(self.Probabilities)

    def createReferenceTable(self):
        valuesUsed = []

        for i in range(len(self.Probabilities[0])):
            self.columnsLength.append(math.floor(self.Probabilities[1][i] * self.maxVal))
        self.columnsLength[0] += 1

        for rowNo in range(1, round(max(self.columnsLength) + 1)):
            row = []
            for j in range(len(self.Probabilities[0])):
                value = round(rowNo / self.Probabilities[1][j])
                value = incrementValueTillNotUsed(value, valuesUsed)
                if rowNo <= self.columnsLength[j]:
                    row.append(value)
                    valuesUsed.append(value)
                else:
                    row.append(None)
            self.referenceTable.append(row)
        self.referenceTable = decrement(self.referenceTable, self.maxVal)
        # print(self.Probabilities[0])
        # print(self.referenceTable)

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
            initialState = self.referenceTable[state[0]-1][self.Probabilities[0].index(symbol)]
        return compressedData + bin(initialState)[2:].zfill(self.precisionBits)

    def decompress(self, comprDat):
        decompressedData = []
        state = [0, '']
        data = 0
        while comprDat:
            try:
                bitsFromString = self.precisionBits - len(bin(state[1]+1)[2:])
            except (TypeError, ValueError):
                bitsFromString = self.precisionBits
            try:
                binaryState = bin(state[1]+1)[2:]
            except TypeError:
                binaryState = ''
            # if state[1] == 6 and comprDat[-2:] == '11':
            #     bitsFromString -= 1
            data = int(binaryState + comprDat[-bitsFromString:], 2)
            comprDat = comprDat[:-bitsFromString]
            state = self.findValueInReferenceTable(data)
            print(state)
            if data != self.maxVal or comprDat:
                decompressedData.append(state[0])

        return decompressedData[::-1]

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

    return byteArray, len(bits) % 8 # druga wartosc zwracana to liczba bitow w ostatnim bajcie, bo nie zawsze to jest8 i sie kod pieprzy


def convertByteArrayToBits(byteArray, numOfLastBits):
    bits = ''
    for byte in byteArray[:-1]:
        bits += str(bin(byte))[2:].zfill(8)
    bits += str(bin(byteArray[-1]))[2:].zfill(numOfLastBits)
    return bits

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
                try:
                    tab[j][i] -= 1
                except TypeError as DecrementNone:
                    pass
    return tab


def bubbleSort(tab2D):
    for i in range(len(tab2D[0]) - 1, 0, -1):
        for j in range(i):
            if tab2D[1][j] < tab2D[1][j + 1]:
                tab2D[1][j], tab2D[1][j + 1] = tab2D[1][j + 1], tab2D[1][j]
                tab2D[0][j], tab2D[0][j + 1] = tab2D[0][j + 1], tab2D[0][j]

    return tab2D
