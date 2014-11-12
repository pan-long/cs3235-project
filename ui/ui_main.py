from Tkinter import *
from PIL import Image, ImageTk
import sys
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
        self.painter.set_canvas(self.paintCanvas)

        if Arguments.isUsingPictureMode:
            Arguments.image = ImageTk.PhotoImage(Image.open(Arguments.picturePath).resize((800, 600)))
            self.paintCanvas.create_image(0, 0, image = Arguments.image, anchor = NW)

        self.processFrame()

    def processFrame(self):
        if not Arguments.windowShouldClose:
            self.painter.getFrame(self.controller)
            self.painter.processFrame()
            # set to 20 FPS
            self.after(50, self.processFrame)
        else:
            self.geometry("450x200+400+300")
            self.paintCanvas.delete("all")

            text_id = self.paintCanvas.create_text(10, 60, anchor=NW)

            text = ''

            if Arguments.isSettingAuthentication:
                text = 'Password Set Successfully!'
            elif Arguments.isGestureVerified:
                text = 'Verification Passed!'
            else:
                text = 'Verification Failed!'

            self.paintCanvas.itemconfig(text_id, text=text, font=("Comic Sans", 30))

            self.after(3000, sys.exit)
