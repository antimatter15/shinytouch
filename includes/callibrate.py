class Callibrate:
    def __init__(self):
        self.clicks = 0
        
    def click(self, x, y):
        global warp_points, perspective
        global window_name, mode

        # Update X&Y co-ordinate of corner
        warp_points[self.clicks] = [x, y]

        if self.clicks==3: # last click
            self.clicks=0
            perspective.update_matrix() # Update Perspective Matrix
            self.writefile() # Write Config file

            # Return to transform mode. Good idea or not?
            cvSetTrackbarPos("Mode", window_name, 2)
            mode=1
        else:
            self.clicks=self.clicks+1

    def writefile(self):
        global warp_points

        buildarray = """# Points to warp to
# top left, top right, bottom right, bottom left
warp_points = """+repr(warp_points)
        
        fh = open("config_warp.py", "w")
        fh.write(buildarray)
        fh.close()
