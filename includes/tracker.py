import opencv
import Image

class Tracker:
    def __init__(self):
        pass
    
    def filter_motion(self, frame, lastframe):
				global motion_threshold
				
				
				gray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
				cvCvtColor(frame, gray, CV_RGB2GRAY );
				
				bitimage=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
				smoothgray = cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
				
				cvSmooth(gray, smoothgray, CV_BLUR, 3, 3);
				
				cvThreshold(smoothgray, bitimage, motion_threshold, 255, CV_THRESH_BINARY)

				#convert Ipl image to PIL image
				im = opencv.adaptors.Ipl2PIL(bitimage)
				pix = im.load()
				
				#TODO: a blob detector (OpenCV? make it work with PYTHON)
				
				
				
				return opencv.adaptors.PIL2Ipl(im)



#based on http://mail.python.org/pipermail/image-sig/2005-September/003559.html
#inspired by http://play.blog2t.net/fast-blob-detection/

def __flood_fill(image, x, y, value):
    "Flood fill on a region of non-BORDER_COLOR pixels."
    BORDER_COLOR = 0
    
    if not image.within(x, y) or image.get_pixel(x, y) == BORDER_COLOR:
        return
    edge = [(x, y)]
    image.set_pixel(x, y, value)
    minx, maxx, miny, maxy = 99999, 0, 99999, 0
    
    while edge:
        newedge = []
        for (x, y) in edge:
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if image.within(s, t) and \
                	image.get_pixel(s, t) not in (BORDER_COLOR, value):
                    image.set_pixel(s, t, value)
                    minx = min(s, minx)
                    maxx = max(s, maxx)
                    miny = min(t, miny)
                    maxy = max(t, maxy)
                    newedge.append((s, t))
        edge = newedge

