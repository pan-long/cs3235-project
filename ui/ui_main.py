from Tkinter import *
from PIL import Image, ImageTk
from leap_motion_sdk import Leap
from logic.leap_painter import LeapPainter
from storage.preference import Arguments

class MainUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = Frame(self)
        self.controller = Leap.Controller()
        self.painter = LeapPainter()
        self.frame.pack(expand = YES, fill = BOTH)
        self.title("Recognito")
        self.geometry("800x600")

        self.paintCanvas = Canvas(self, width = "800", height = "600")
        self.paintCanvas.pack(expand = YES, fill=BOTH)

        if Arguments.isUsingPictureMode:
            self.image = ImageTk.PhotoImage(Image.open(Arguments.picturePath).resize((800, 600)))
            self.paintCanvas.create_image(0, 0, image = self.image, anchor = NW)

        self.painter.set_canvas(self.paintCanvas)

        self.processFrame()

    def processFrame(self):
        self.painter.getFrame(self.controller)
        self.painter.processFrame()
        # set to 20 FPS
        self.after(50, self.processFrame)