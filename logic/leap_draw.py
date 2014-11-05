from Tkinter import Frame, Canvas, YES, BOTH
from leap_motion_sdk import Leap

class LeapListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        self.paintCanvas.delete("all")
        frame = controller.frame()

        interactionBox = frame.interaction_box
        
        for pointable in frame.pointables:
            normalizedPosition = interactionBox.normalize_point(pointable.tip_position)
            if(pointable.touch_distance > 0 and pointable.touch_zone != Leap.Pointable.ZONE_NONE):
                color = self.rgb_to_hex((0, 255 - 255 * pointable.touch_distance, 0))
                
            elif(pointable.touch_distance <= 0):
                color = self.rgb_to_hex((-255 * pointable.touch_distance, 0, 0))
                #color = self.rgb_to_hex((255,0,0))
                
            else:
                color = self.rgb_to_hex((0,0,200))
                
            self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 40, 40, color)

    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval( x, y, x + width, y + height, fill = color, outline = "")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas
        
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb
