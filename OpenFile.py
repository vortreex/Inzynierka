def openFileAsByteArray(filePath):
    f = open(filePath, 'rb')
    return list(f.read())
