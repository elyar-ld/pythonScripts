from random import seed
from random import randint
from PIL import Image
import sys

wrapperImg = Image.open(sys.argv[1])
pixelsWrapper = wrapperImg.load()

encodedImg = open(sys.argv[2], "rb") 
dataEncoded = encodedImg.read()

encodedImg.close()

wrapperLength = wrapperImg.size[0]*wrapperImg.size[1]

if((wrapperLength*3 - 24) < len(dataEncoded)*8):
	print("Error: image to encode size is larger than wrapper capacity. The capacity of current wrapper image is: "+str((wrapperImg.size[0]*wrapperImg.size[1]*3 - 24)/8)+" bytes")
	sys.exit()
if(len(dataEncoded) > 1024*2048):
	print("Error: image to encode size is larger than 2MB: "+str((wrapperImg.size[0]*wrapperImg.size[1]*3 - 24)/8)+" bytes")
	sys.exit()

encodedBinArr = []

bytesNum = len(dataEncoded)
#first 24 bits is the number of bytes of encoded image
for i in range(24):
	encodedBinArr.append(0)
	a = 8388608 >> i
	if (bytesNum & a) != 0:
		encodedBinArr[i] = 1

for byte in dataEncoded:
	encodedBinArr.append(byte >> 7)
	for x in range(6,0,-1):
		encodedBinArr.append((byte >> x) & 1)	
	encodedBinArr.append(byte & 1)

wrapperByteArr = []

for i in range(wrapperImg.size[0]):
	for j in range(wrapperImg.size[1]):
		wrapperByteArr.append(pixelsWrapper[i,j][0])
		wrapperByteArr.append(pixelsWrapper[i,j][1])
		wrapperByteArr.append(pixelsWrapper[i,j][2])

wrapperByteArrLen = len(wrapperByteArr)
seed(int.from_bytes(bytes(sys.argv[3], encoding="utf-8"), byteorder="big"))

randomPositions = [x for x in range(wrapperByteArrLen)]
m = len(randomPositions)
while (m):
	m -= 1
	i = randint(0, m)
	randomPositions[m], randomPositions[i] = randomPositions[i], randomPositions[m]
randomPositions = randomPositions[:len(encodedBinArr)]

for i in range(len(encodedBinArr)):
	a = encodedBinArr[i] & 1
	b = wrapperByteArr[randomPositions[i]] & 1
	if a != b:
		wrapperByteArr[randomPositions[i]] ^= 1

result = Image.new( wrapperImg.mode, wrapperImg.size)
pixelsResult = result.load()

ind = 0
for i in range(wrapperImg.size[0]):
	for j in range(wrapperImg.size[1]):
		pixelsResult[i,j] = (wrapperByteArr[ind],wrapperByteArr[ind+1],wrapperByteArr[ind+2])
		ind += 3

result.save('resultEncoded.png')
print("Finished!")
