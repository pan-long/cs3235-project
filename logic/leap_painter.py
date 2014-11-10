from Tkinter import Frame, Canvas, YES, BOTH
from leap_motion_sdk import Leap

class LeapPainter():
    lastFrameId = 0

    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval(x, y, x + width, y + height, fill = color, outline = "")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas
        
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def getFrame(self, controller):
        self.frame = controller.frame

    def processFrame(self):
        if self.frame.id == self.lastFrameId:
            return
        else:
            self.paintCanvas.delete("all")
            frame = self.frame
            interactionBox = frame.interaction_box
        
            for pointable in frame.pointables:
                normalizedPosition = interactionBox.normalize_point(pointable.tip_position)
                if(pointable.touch_distance > 0 and pointable.touch_zone != Leap.Pointable.ZONE_NONE):
                    color = self.rgb_to_hex((0, 255 - 255 * pointable.touch_distance, 0))
                    
                elif(pointable.touch_distance <= 0):
                    color = self.rgb_to_hex((-255 * pointable.touch_distance, 0, 0))
                    
                else:
                    color = self.rgb_to_hex((0,0,200))
                    
                self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 40, 40, color)

            self.lastFrameId = frame.id