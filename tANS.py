import sys
import os
import OpenFile

print('Kompresuje metoda tANS plik: ' + str(sys.argv[1]))

path = os.curdir + '/' + str(sys.argv[1])
f = OpenFile.openFileAsByteArray(path)


f.close()
