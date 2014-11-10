from Tkinter import Tk, Frame, Canvas, YES, BOTH
from leap_motion_sdk import Leap
from logic.leap_painter import LeapPainter

class MainUI(Tk):
    def __init__( self ):
        Tk.__init__(self)
        self.frame = Frame(self)
        self.controller = Leap.Controller()
        self.painter = LeapPainter()
        self.frame.pack(expand = YES, fill = BOTH)
        self.title("Recognito")
        self.geometry("800x600")

        self.paintCanvas = Canvas(self, width = "800", height = "600")
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)

        self.processFrame()

    def processFrame(self):
        self.painter.getFrame(self.controller)
        self.painter.processFrame()
        # set 20 FPS
        self.after(50, self.processFrame)