from PIL import Image
import sys

img = Image.open(sys.argv[1])
pixelsImg = img.load()

img2 = Image.new(img.mode,img.size)
pixelsImg2 = img2.load()
for i in range(img.size[0]):
	for j in range(img.size[1]):
		a = 0xFF
		b = 0xFF
		c = 0xFF
		if pixelsImg[i,j][0] & 1 == 0:
			a = 0
		if pixelsImg[i,j][1] & 1 == 0:
			b = 0
		if pixelsImg[i,j][2] & 1 == 0:
			c = 0
		pixelsImg2[i,j] = (a, b, c)
img2.show()