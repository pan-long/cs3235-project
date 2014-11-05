from Tkinter import Frame, Canvas, YES, BOTH
from leap_motion_sdk import Leap
from logic.leap_draw import LeapListener

class MainUI(Frame):
    def __init__( self ):
        Frame.__init__( self )
        self.leap = Leap.Controller()
        self.painter = LeapListener()
        self.leap.add_listener(self.painter)
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Touch Points" )
        self.master.geometry( "800x600" )
      
        # create Canvas component
        self.paintCanvas = Canvas( self, width = "800", height = "600" )
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)
