import opencv
import Image
import ImageDraw

def fdivide(a,b):
  if b == 0:
    return 1.0
  return float(a)/float(b)


def colorDiffGrade(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return abs(r) + abs(g) + abs(b)

  
def colorDiffAverage(c,d):
  r = c[0]-d[0]
  g = c[1]-d[1]
  b = c[2]-d[2]
  return (r + g + b)/3.0
  
  
def colorTestRGB(frame, pix, x, y):
  try:
    c = pix[x+10,y] #reflection
    d = pix[x+10,y-15] #background
    t = pix[x-5,y] #color of the finger
    
    irIM = fdivide(c[0]-d[0],t[0]-d[0])
    igIM = fdivide(c[1]-d[1],t[1]-d[1])
    ibIM = fdivide(c[2]-d[2],t[2]-d[2])
    
    print irIM+igIM+ibIM
    if irIM+igIM+ibIM < 10:
      return True
    
    return False
  except IndexError:
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
          if colorTestRGB(frame, bigpix, blob[0]*2, blob[1]+blob[3]) is True:
            cvRectangle(frame, point1, point2, cvScalar(0,0,255))
          else:
            cvRectangle(frame, point1, point2, cvScalar(0,255,255))
          
        return frame

