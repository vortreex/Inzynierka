def openFileAsByteArray(filePath):
    f = open(filePath, 'rb')
    byteMap = list(f.read())
    f.close()
    return byteMap
