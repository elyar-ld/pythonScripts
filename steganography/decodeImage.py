from PIL import Image
from numpy import random as rn
from numpy import arange
from itertools import product
import sys

encoded = Image.open(sys.argv[1])
pixelsEncoded = encoded.load()

rn.seed(int.from_bytes(bytes(sys.argv[2], encoding="utf-8"), byteorder="big") % 2**32)

range1 = list(rn.permutation(arange(encoded.size[0])))
range2 = list(rn.permutation(arange(encoded.size[1])))
range3 = list(rn.permutation(arange(3)))

randomIndexes = (list(product(*[range1, range2, range3])))

size = 0
for i in range(24):
	ranIndex = randomIndexes[i]
	pixel = pixelsEncoded[int(ranIndex[0]),int(ranIndex[1])]
	size += (pixel[int(ranIndex[2])] & 1) * (8388608 >> i)
print(size)	
randomIndexes = randomIndexes[24:size*8+24]

decodedIntArr = []
ind = 0
for x in range(size):
	byteInt = 0
	for y in range(8):
		ranIndex = randomIndexes[ind]
		val = pixelsEncoded[int(ranIndex[0]),int(ranIndex[1])][int(ranIndex[2])] & 1

		byteInt += val*(0b10000000 >> y)

		ind += 1
	decodedIntArr.append(byteInt)

print(decodedIntArr[:100])
with open('resultDecoded', 'wb') as output:
    output.write(bytearray(decodedIntArr))
