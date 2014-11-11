from Tkinter import *
from PIL import Image, ImageTk
from leap_motion_sdk import Leap
from storage.storage import Storage
from storage.preference import Arguments

class LeapPainter():
    lastFrameId = 0
    started = False
    isPressed = False
    point_coord = []
    isLeftHand = False
    idleCounter = 0
    lastIsIdle = False
    points = []

    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval(x, y, x + width, y + height, fill = color, outline = "")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas
        
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def getFrame(self, controller):
        self.currentFrame = controller.frame()

    def processFrame(self):
        if self.currentFrame.id == self.lastFrameId:
            # if we requesting the frame too fast and get the same frame as last requesting,
            # simply ignore this frame as we have processed already
            return
        else:
            # any process of frame from Leap should goes here
            self.paintCanvas.delete("all")
            if Arguments.isUsingPictureMode:
                self.image = ImageTk.PhotoImage(Image.open(Arguments.picturePath).resize((800, 600)))
                self.paintCanvas.create_image(0, 0, image = self.image, anchor = NW)
            
            frame = self.currentFrame
            interactionBox = frame.interaction_box
        
            for pointable in frame.pointables:
                normalizedPosition = interactionBox.normalize_point(pointable.tip_position)
                if(pointable.touch_distance > 0 and pointable.touch_zone != Leap.Pointable.ZONE_NONE):
                    color = self.rgb_to_hex((0, 255 - 255 * pointable.touch_distance, 0))
                    
                elif(pointable.touch_distance <= 0):
                    color = self.rgb_to_hex((-255 * pointable.touch_distance, 0, 0))
                    
                else:
                    color = self.rgb_to_hex((0,0,200))
                
                # if normalizedPosition.x is not greater than 0, the points will not 
                # disapear in the canvas, but simply go along the edge
                if normalizedPosition.x > 0 and normalizedPosition.y > 0: 
                    self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 40, 40, color)

            if Arguments.isUsingBinaryMode:
                # if it is using left/right hand mode, simply use binary value for left/right hand, 
                # any hand present will result in "pressed" status
                if len(frame.hands) == 0:
                    # if no hand present 
                    if not lastIsIdle:
                        points.append(isLeftHand)
                        idleCounter += 1

            self.lastFrameId = frame.id
