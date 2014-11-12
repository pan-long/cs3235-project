from Tkinter import *
from PIL import Image, ImageTk
from operator import attrgetter
from leap_motion_sdk import Leap
from storage.storage import Storage
from storage.preference import Arguments

class LeapPainter():
	lastFrameId = 0

	# has the gesture started
	started = False

	# is currently pressed?
	isPressed = False

	isLeftHand = False

	isNextBinaryGesture = True

	# how many consecutive plain frames we have?
	# if it hits a certain number, we should stop gesturing and start verifying
	idleCounter = 0

	# all the points we have stores in gestures
	points = []
	lines = []

	def draw(self, x, y, width, height, color):
		self.paintCanvas.create_oval(x, y, x + width, y + height, fill = color, outline = "")

	def draw_line(self, x1, y1, x2, y2, width, color):
		self.paintCanvas.create_line(x1, y1, x2, y2, width = width, dash = True)

	def set_canvas(self, canvas):
		self.paintCanvas = canvas
		
	def rgb_to_hex(self, rgb):
		return '#%02x%02x%02x' % rgb

	def getFrame(self, controller):
		self.currentFrame = controller.frame()

	def redraw(self):
		# any process of frame from Leap should goes here
		self.paintCanvas.delete("all")
		# redraw the background image
		if Arguments.isUsingPictureMode:
			self.image = ImageTk.PhotoImage(Image.open(Arguments.picturePath).resize((800, 600)))
			self.paintCanvas.create_image(0, 0, image = self.image, anchor = NW)
		
		# redraw what we have stored in our gesture
		if Arguments.isUsingPictureMode:# or Arguments.isUsingGestureMode:
			color = self.rgb_to_hex((200, 0, 0))
			for point in self.points:
				self.draw(point.x * 800, 600 - point.y, 40, 40, color)

		# redraw lines that we have stored
		if Arguments.isUsingPictureMode:
			color = self.rgb_to_hex((160, 0, 0))
			for line in self.lines:
				self.draw_line(line[0].x, line[0].y, line[1].x, line[1].y, 10, color)	

	def processingPictureMode(self, frame):
		# TO-DO

		return

	def processingBinaryMode(self, frame):
		if len(frame.hands) > 0 and self.isNextBinaryGesture:
			self.points.append(frame.hands[0].is_left)
			self.isNextBinaryGesture = False
		if Arguments.isSettingAuthentication:
			Storage.write(self.points, "binary.obj")
		return 

	def processingGestureMode(self, frame):
		# TO-DO
		coordinate = []
		if len(frame.hands) == 2:
			if frame.hands[0].is_left:
				for i in range(0, len(frame.hands[0].fingers)):
					coordinate.append(frame.hands[0].fingers[i].tip_position.x)
					coordinate.append(frame.hands[0].fingers[i].tip_position.y)
					coordinate.append(frame.hands[0].fingers[i].tip_position.z)
				for i in range(len(frame.hands[0].fingers), 5):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
			else:
				for i in range(0, len(frame.hands[1].fingers)):
					coordinate.append(frame.hands[1].fingers[i].tip_position.x)
					coordinate.append(frame.hands[1].fingers[i].tip_position.y)
					coordinate.append(frame.hands[1].fingers[i].tip_position.z)
				for i in range(len(frame.hands[1].fingers), 5):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
		elif len(frame.hands) == 1:
			if frame.hands[0].is_left:
				for i in range(0, len(frame.hands[0].fingers)):
					coordinate.append(frame.hands[0].fingers[i].tip_position.x)
					coordinate.append(frame.hands[0].fingers[i].tip_position.y)
					coordinate.append(frame.hands[0].fingers[i].tip_position.z)
				for i in range(len(frame.hands[0].fingers), 10):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
			else:
				for i in range(0, 5):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
				for i in range(0, len(frame.hands[0].fingers)):
					coordinate.append(frame.hands[0].fingers[i].tip_position.x)
					coordinate.append(frame.hands[0].fingers[i].tip_position.y)
					coordinate.append(frame.hands[0].fingers[i].tip_position.z)
				for i in range(len(frame.hands[0].fingers) + 5, 10):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
		else:
			return

		self.points.append(coordinate)
		print self.points
		if Arguments.isSettingAuthentication:
			Storage.write(self.points, "gesture.obj")
		return

	def verify(self):
		if Arguments.isUsingPictureMode:
			# TO-DO
			return True
		elif Arguments.isUsingBinaryMode:
			# May change to another filename
			benchmark = Storage.read("binary.obj")
			print ("Current: %s" % self.points)
			# print ("Benchmark: %s" % benchmark)
			if benchmark == self.points:
				print "Verification Passed."
				return True
			else :
				print "Verification Failed."
				return False
		elif Arguments.isUsingGestureMode:
			# TO-DO
			benchmark = Storage.read("gesture.obj")
			# If numbers of frames have a significant difference, reject immediately.
			if (len(self.points) < len(benchmark) * 0.5) or (len(self.points) > len(benchmark) * 2):
				print "Verification Failed."
				return False
			benchmarking = 0.0
			for i in range(1, len(benchmark)):
				for j in range(0, 30):
					benchmarking += pow(benchmark[i][j] - benchmark[i-1][j], 2)
			k = 100.0
			threshold = min(k * pow(len(benchmark) * 30, 1.5), benchmarking * 0.9)
			delta = 0.0
			for i in range(1, min(len(benchmark), len(self.points))):
				for j in range(0, 30):	
					delta += pow((benchmark[i][j] - benchmark[i-1][j]) 
						- (self.points[i][j] - self.points[i-1][j]), 2)

			for i in range(min(len(benchmark), len(self.points)), max(len(benchmark), len(self.points))):
				if len(benchmark) == max(len(benchmark), len(self.points)):
					for j in range(0, 30):
						delta += pow(benchmark[i][j] - benchmark[i-1][j], 2)
				else:
					for j in range(0, 30):
						delta += pow(self.points[i][j] - self.points[i-1][j], 2)

			print "delta: %s" % delta
			print "benchmarking: %s" % benchmarking
			print "threshold: %s" % threshold
			if delta <= threshold:
				print "Verification Passed."
			else:
				print "Verification Failed."
			return (delta <= threshold)
			
		

	def processFrame(self):
		if self.currentFrame.id == self.lastFrameId:
			# if we requesting the frame too fast and get the same frame as last requesting,
			# simply ignore this frame as we have processed already
			self.idleCounter += 1
			return
		else:
			self.redraw()

			frame = self.currentFrame
			# if the frame is plain, simply add counter
			if len(frame.pointables) == 0:
				self.idleCounter += 1
				self.isNextBinaryGesture = True
				if self.idleCounter >= 30:
					# do verification and display something secret
					if not Arguments.isSettingAuthentication:
						self.verify()
					sys.exit(0)
				return  

			# if this frame is not plain, reset the counter to 0
			self.idleCounter = 0

			if Arguments.isUsingPictureMode:
				self.processingPictureMode(frame)
			elif Arguments.isUsingBinaryMode:
				self.processingBinaryMode(frame)
			elif Arguments.isUsingGestureMode:
				self.processingGestureMode(frame)
			else:
				print 'No mode specified, using picture mode by default'
				self.processingPictureMode(frame)

			# set current frame id as the last frame id
			self.lastFrameId = frame.id
