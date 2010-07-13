

import Image, ImageDraw





#based on http://mail.python.org/pipermail/image-sig/2005-September/003559.html
#inspired by http://play.blog2t.net/fast-blob-detection/
def get_blobs(im, skip = 0):
  pix = im.load()
  width, height = im.size
  blobs = []
  def within(x, y):
    return x > 0 and y > 0 and x < width and y < height

  for px in range(0, width, skip+1):
    for py in range(0, height, skip+1):
      if pix[px, py] != 0:
        edge = [(px, py)]
        pix[px, py] = 0
        minx, maxx, miny, maxy = 99999, 0, 99999, 0
        while edge:
          newedge = []
          for (x, y) in edge:
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
              if within(s, t) and pix[s, t] != 0:
                pix[s, t] = 0
                minx = min(s, minx)
                maxx = max(s, maxx)
                miny = min(t, miny)
                maxy = max(t, maxy)
                newedge.append((s, t))
          edge = newedge
          
        blobwidth = maxx-minx
        blobheight = maxy-miny
        blobs.append((minx, miny, blobwidth, blobheight))
  return blobs


newim = Image.open('blobdetect.png')
im = newim.convert("1")
draw = ImageDraw.Draw(newim)
import time
start = time.time()
blobs = get_blobs(im,2)
end = time.time()
print "Done in ",end-start," seconds"  

for blob in blobs:
  draw.rectangle((blob[0], blob[1], blob[0]+blob[2], blob[1]+blob[3]), outline=128)


newim.save('blobout.png','png')
