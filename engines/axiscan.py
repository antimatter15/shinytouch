import Image
import ImageFilter

imorig = Image.open('Selection_010.png')

im = imorig.copy()#.filter(ImageFilter.BLUR)

barwidth = 40
pix = im.load()
new = imorig.load()
width, height = im.size


for m in range(100, 200, 5):
	for x in range(0, width):
		for y in range(0, height):
			c1 = pix[x,y]
			c1s = c1[0]+c1[1]+c1[2]
			if c1s > m*3:
				new[x,y] = (10*(m-100),10*(m-100),255)
			




"""
halfbar = barwidth/2
for x in range(halfbar, width - halfbar):
	for y in range(0, height):
		c1 = pix[x-halfbar,y]
		c2 = pix[x+halfbar,y]
		c1s = c1[0]+c1[1]+c2[2]
		c2s = c2[0]+c2[1]+c2[2]
		if abs(c1s - c2s) < 80 and abs(c1s - c2s) > 30 and c1s < 150:
			new[x-halfbar,y] = (barwidth*5,barwidth*5,255)
			#new[x+halfbar,y] = (barwidth*5,255, barwidth*5)
#"""

imorig.save('output.png','png')
		
