import opencv
import Image
import ImageDraw
import colorsys

#convert to HSV, yay python standard library!
def hsv(c):
  return colorsys.rgb_to_hsv(c[0]/255.0, c[1]/255.0, c[2]/255.0)

#grade hue by diff
def hueDiffGrade(c, d):
  chsv = hsv(c)
  dhsv = hsv(d)
  return abs(dhsv[2]-chsv[2])+abs(dhsv[1]-chsv[1])+abs(dhsv[0]-chsv[0])
  
  

def measureLength(frame, pix, x,y,xi=0,yi=1,r=25,smarty=30): #start x, start y, x incrementer, y incrementer
  def setpixel(x,y,color):
    cvRectangle(frame, cvPoint(x, y), cvPoint(x+1,y+1), cvScalar(color[0],color[1],color[2]))
    
  try:
    xt = 0
    yt = 0
    #while colorDiffGrade(pix[x+xt,y+yt],pix[x+xt+xi,y+yt+yi]) < r: #use a more fine tuned function
    if smarty > 0:
      bgcolor = pix[x,y-15]
      setpixel(x,y-15,(0,0,255))
    else:
      bgcolor = pix[x,y+15]
      #pix[x,y+15] = (0,0,255)
      setpixel(x,y+15, (0,0,255))
    targetcolor = avg_color((pix[x,y],pix[x+1,y],pix[x,y+1]))
    print hueTriDiff(pix[x+xt+xi,y+yt+yi],targetcolor,bgcolor)
    while hueTriDiff(pix[x+xt+xi,y+yt+yi],targetcolor,bgcolor) < -0:
      setpixel(x+xt,y+yt,(255,255,255,255))
      
      
      xt += xi
      yt += yi
      if xt + x < 5 or xt + x > 630 or yt+y < 5 or yt+y > 470:
        return 0
        #return yt+xt
    return yt+xt
  except IndexError:
    return 0

def avg_color(colors):
  r = 0.0
  g = 0.0
  b = 0.0
  for color in colors:
    r += color[0]
    g += color[1]
    b += color[2]
  l = len(colors)
  return (r/l, g/l, b/l)

def in_range(x,y,space=20):
  global width, height
  return x < width - space and x > space and y > space and y < height - space

def colorTriDiff(c, f, s):
  return (valueTriDiff(c[0], f[0], s[0]) + valueTriDiff(c[1], f[1], s[1]) + valueTriDiff(c[2], f[2], s[2]))/3.0
  
def hueTriDiff(c, f, s):
  return valueTriDiff(hsv(c)[0], hsv(f)[0], hsv(s)[0])  

def valueTriDiff(compare, first, second):
  return abs(first - compare) - abs(second - compare)


def colorTestLength(frame, pix, x, y):
  c = pix[x+5,y]
  d = pix[x+5,y-10]
  t = pix[x-5,y]
  
  #draw.line(((x-4,y),(x+4,y)),fill=(255,255,0))
  #draw.line(((x,y-4),(x,y+4)),fill=(255,255,0))
  
  sumfs = 0
  sy = y
  fy = y
  
  for xpix in range(6,6+20):
    fpeak = measureLength(frame, pix, x-xpix,fy)
    speak = measureLength(frame, pix, x+xpix,sy)
    flen =  fpeak+abs(measureLength(frame, pix, x-xpix,fy-1,yi=-1,smarty=-30))
    slen =  speak+abs(measureLength(frame, pix, x+xpix,sy-1,yi=-1,smarty=-30))
    
    newfy = fy + fpeak - (flen/2)
    newsy = sy + speak - (slen/2)
    
    if in_range(x-xpix, newfy) and in_range(x + xpix, newsy):
      pix[x-xpix, newfy] = (255,0,0)
      pix[x+xpix, newsy] = (255,0,0)
      if abs(sy - newsy) < 10:
        sy = newsy
      if abs(fy - newfy) < 10:
        fy = newfy
      #sy = newsy
      #fy = newfy
      
    
    #print flen-slen
    minlen = min(flen, slen)
    maxlen = max(flen, slen)
    if minlen != 0:
      sumfs += 5*(20-(xpix-6))  * (maxlen/minlen - 1)
    else:
      sumfs += 0
    #sumfs += 42*(abs(flen/(slen+1))-1) #basic ratio 
    #sumfs += abs(flen-slen) #diff
    #sumfs += (flen-slen)*(flen-slen)*0.2 #square diff
    
    #if abs(flen-slen) > 20:
    #  return False
  #print sumfs / abs(float(6-15))
  
  maxfs = 60
  
  avgfs = sumfs / abs(float(20))
  
  cvLine(frame, cvPoint(150,20), cvPoint(int(150+avgfs),20), cvScalar(255,0,0), 10);
  cvLine(frame, cvPoint(int(150+maxfs), 0), cvPoint(int(150+maxfs), 40), cvScalar(0,0,255), 5);
  
  
  if avgfs < maxfs:
    return False
  return True

#divide as floats and return 0 if divide by zero
def fdivide(a,b):
  if b == 0:
    return 1.0
  return float(a)/float(b)



def colorTestHue( frame, pix, x, y):
  reflect = -15
  reflect_range = 20
  background_top = 30
  
  def setpixel(x,y,color):
    cvRectangle(frame, cvPoint(x, y), cvPoint(x+1,y+1), cvScalar(color[0],color[1],color[2]))
  
  try:  
    c = pix[x+reflect,y] #reflection
    d = pix[x+reflect,y-background_top] #background
    t = pix[x-5,y] #color of the finger
  except IndexError:
    return False
    
  cdg = 200 *(abs(hueDiffGrade(c,d)))
  
  print "Finger ",t
  print "Reflection ",c
  print "Background ",d
    
  setpixel(x+reflect,y, (255,255,255))
  setpixel(x+reflect,y-background_top, (255,0,255,255))
  
  
  #cvRectangle(frame, cvPoint(40,0), cvPoint(80,40), cvScalar(int(c[0]), int(c[1]), int(c[2])))
  #cvRectangle(frame, cvPoint(80,0), cvPoint(120,40), cvScalar(int(d[0]), int(d[1]), int(d[2])))
  
  print "CDG IS ",int(cdg)
  cvLine(frame, cvPoint(10, 20+40), cvPoint(int(cdg), 20+40), cvScalar(255,0,0), 10)

  cvLine(frame, cvPoint(int(reflect_range), 40), cvPoint(int(reflect_range), 80),cvScalar(0,0,255))

  #draw.text((0,20), str(cdg), fill=(0,0,0))

  if cdg > reflect_range:
    return True
  return False
  


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
        blobs.append((minx, miny, maxx, maxy))
  return blobs



class Tracker:
    def __init__(self):
        pass
        
        
    def filter_motion(self, frame, lastframe):
        global motion_threshold
        
        diffImage=cvCreateImage(cvSize(width, height), 8, 3)
        #gray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        #cvCvtColor(frame, gray, CV_RGB2GRAY );
        
        #bitimage=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        #smoothgray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        
        #cvSmooth(gray, smoothgray, CV_BLUR, 6, 6);
        
        #cvThreshold(smoothgray, bitimage, motion_threshold, 255, CV_THRESH_BINARY)

        cvAbsDiff(frame,lastframe,diffImage);

        return diffImage


    def process_image(self, frame, lastframe):
        global motion_threshold
        
        
        gray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        cvCvtColor(frame, gray, CV_RGB2GRAY );
        
        bitimage=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        smoothgray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        
        cvSmooth(gray, smoothgray, CV_BLUR, 6, 6);
        
        cvThreshold(smoothgray, bitimage, motion_threshold, 255, CV_THRESH_BINARY)

        #convert Ipl image to PIL image
        im = opencv.adaptors.Ipl2PIL(bitimage)
        colorim = opencv.adaptors.Ipl2PIL(frame)
        bigpix = colorim.load()
        
        tinyim = im.convert("1").resize((im.size[0]/2,im.size[1]/2))
        #draw = ImageDraw.Draw(im)
        
        #TODO: a blob detector (OpenCV? make it work with PYTHON)
        for blob in get_blobs(tinyim, 5):
          point1 = cvPoint(blob[0]*2, blob[1]*2)
          point2 = cvPoint(blob[2]*2, blob[3]*2)
          cvRectangle(frame, cvPoint(blob[0]*2-5, blob[1]+blob[3]-5), cvPoint(blob[0]*2+5, blob[1]+blob[3]+5), cvScalar(255,255,255))
          if colorTestHue(frame, bigpix, blob[0]*2, blob[1]+blob[3]) is True:
            cvRectangle(frame, point1, point2, cvScalar(0,0,255))
          else:
            cvRectangle(frame, point1, point2, cvScalar(0,255,255))
          
        return frame

