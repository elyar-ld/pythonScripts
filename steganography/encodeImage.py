from PIL import Image
from numpy import random as rn
from numpy import arange
from itertools import product
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

rn.seed(int.from_bytes(bytes(sys.argv[3], encoding="utf-8"), byteorder="big") % 2**32)

range1 = list(map(int,list(rn.permutation(arange(wrapperImg.size[0])))))
range2 = list(map(int,list(rn.permutation(arange(wrapperImg.size[1])))))
range3 = list(map(int,list(rn.permutation(arange(3)))))

randomIndexes = (list(product(*[range1, range2, range3])))[:len(dataEncoded)*8+24]

ind = 0
while ind < 24:
	ranIndex = randomIndexes[ind]
	pixel = list(pixelsWrapper[ranIndex[0], ranIndex[1]])
	
	a = 8388608 >> ind  						#it starts as 0b100000000000000000000000 = 8388608
	b = (len(dataEncoded) & a) >> (23 - ind) 	#bit of Size that will be encoded
	p = pixel[ranIndex[2]] & 1 #least significant bit of rgb pixel

	if (b ^ p): #least significant bit of rgb pixel changes only if different of bit b 
		pixel[ranIndex[2]] = (pixel[ranIndex[2]] >> 1 << 1) + b
	pixelsWrapper[ranIndex[0], ranIndex[1]] = tuple(pixel)
	ind += 1

for byte in dataEncoded:
	for i in range(7,-1,-1):
		ranIndex = randomIndexes[ind]
		pixel = list(pixelsWrapper[ranIndex[0], ranIndex[1]])
		pixel[ranIndex[2]] = (pixel[ranIndex[2]] >> 1 << 1) + ((byte >> i) & 1)
		pixelsWrapper[ranIndex[0], ranIndex[1]] = tuple(pixel)
		ind += 1

wrapperImg.save('resultEncoded.png')

print("Finished!")
