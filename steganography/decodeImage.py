from random import seed
from random import randint
from PIL import Image
import sys

encoded = Image.open(sys.argv[1])
pixelsEncoded = encoded.load()

encodedBinArr = []

for i in range(encoded.size[0]):
	for j in range(encoded.size[1]):
		encodedBinArr.append(pixelsEncoded[i,j][0] & 1)
		encodedBinArr.append(pixelsEncoded[i,j][1] & 1)
		encodedBinArr.append(pixelsEncoded[i,j][2] & 1)

encodedBinArrLen = len(encodedBinArr)
visited = [0]*encodedBinArrLen

seed(int.from_bytes(bytes(sys.argv[2], encoding="utf-8"), byteorder="big"))

randomPositions = [x for x in range(len(encodedBinArr))]
m = len(randomPositions)
while (m):
	m -= 1
	i = randint(0, m)
	randomPositions[m], randomPositions[i] = randomPositions[i], randomPositions[m]

size = 0
for x in range(24):
	size += encodedBinArr[randomPositions[x]] * (8388608 >> x)
randomPositions = randomPositions[24:size*8+24]

decodedIntArr = []
for x in range(size):
	byteInt = 0
	for y in range(8):
		byteInt += encodedBinArr[randomPositions[8*x+y]]*(0b10000000 >> y)
	decodedIntArr.append(byteInt)

with open('resultDecoded', 'wb') as output:
    output.write(bytearray(decodedIntArr))
