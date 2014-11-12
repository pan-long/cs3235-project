from Tkinter import *
from PIL import Image, ImageTk
import math
from operator import attrgetter
from leap_motion_sdk import Leap
from storage.storage import Storage
from storage.preference import Arguments

class Point:
	x = 0.0
	y = 0.0

	def __init__(self, x, y):
		self.x = x
		self.y = y

class LeapPainter():
	lastFrameId = 0

	# has the gesture started
	started = False

	# is currently pressed?
	isPressed = False

	isLeftHand = False

	# how many consecutive plain frames we have?
	# if it hits a certain number, we should stop gesturing and start verifying
	idleCounter = 0

	# all the points we have stores in gestures
	points = []
	printablePoints = []
	lines = []

	def printd(self, string):
		if Arguments.isUsingDebugMode:
			print string

	def draw(self, x, y, width, height, color):
		self.paintCanvas.create_oval(x, y, x + width, y + height, fill = color, outline = "")

	def draw_line(self, x1, y1, x2, y2, width, color):
		self.paintCanvas.create_line(x1, y1, x2, y2, width = width, fill = color, dash = True)

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
			self.paintCanvas.create_image(0, 0, image = Arguments.image, anchor = NW)
		
		# redraw what we have stored in our gesture
		if Arguments.isUsingPictureMode or Arguments.isUsingGestureMode:
			color = self.rgb_to_hex((100, 160, 0))
			for point in self.printablePoints:
				self.draw(point.x * 800, 600 - point.y * 600, 30, 30, color)

		# redraw lines that we have stored
		if Arguments.isUsingPictureMode:
			color = self.rgb_to_hex((160, 0, 0))
			for line in self.lines:
				self.draw_line(line[0].x * 800, 600 - line[0].y * 600, line[1].x * 800, 600 - line[1].y * 600, 5, color)	

	def processingPictureMode(self, frame):
		interactionBox = frame.interaction_box

		if len(frame.hands) > 0:
			pointFinger = frame.hands[0].fingers.frontmost
			normalizedPosition = interactionBox.normalize_point(pointFinger.tip_position)

			if pointFinger.touch_distance > 0 and pointFinger.touch_zone != Leap.Pointable.ZONE_NONE:
				color = self.rgb_to_hex((0, 255 - 255 * pointFinger.touch_distance, 0))
				
			elif pointFinger.touch_distance <= 0:
				color = self.rgb_to_hex((-255 * pointFinger.touch_distance, 0, 0))
				
			else:
				color = self.rgb_to_hex((0,0,200))

			self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 30, 30, color)

			if pointFinger.touch_distance < Arguments.depthForPictureMode:
				self.isPressed = True

			elif self.isPressed:
				self.isPressed = False
				point = Point(normalizedPosition.x, normalizedPosition.y)
				self.points.append(point)
				self.printablePoints.append(normalizedPosition)
				if len(self.printablePoints) > 1:
					p1 = self.printablePoints[-1]
					p2 = self.printablePoints[-2]
					self.lines.append([p1, p2])

				if Arguments.isSettingAuthentication:
					Storage.write(self.points, "picture.data")

			else:
				return
		else:
			return

	def processingBinaryMode(self, frame):
		if len(frame.hands) > 0:
			# self.printd(str(frame.hands[0].palm_position.z))
			if (not self.isPressed) and (frame.hands[0].palm_position.z < Arguments.depthForBinaryMode):
				self.points.append(frame.hands[0].is_left)
				self.printd(self.points)
				self.isPressed = True

				if Arguments.isSettingAuthentication:
					Storage.write(self.points, "binary.data")

			elif frame.hands[0].palm_position.z >= Arguments.depthForBinaryMode:
				self.isPressed = False

		return 

	def processingGestureMode(self, frame):
		coordinate = []
		interactionBox = frame.interaction_box

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
				for i in range(0, len(frame.hands[1].fingers)):
					coordinate.append(frame.hands[1].fingers[i].tip_position.x)
					coordinate.append(frame.hands[1].fingers[i].tip_position.y)
					coordinate.append(frame.hands[1].fingers[i].tip_position.z)
				for i in range(len(frame.hands[1].fingers), 5):
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
				for i in range(0, len(frame.hands[0].fingers)):
					coordinate.append(frame.hands[0].fingers[i].tip_position.x)
					coordinate.append(frame.hands[0].fingers[i].tip_position.y)
					coordinate.append(frame.hands[0].fingers[i].tip_position.z)
				for i in range(len(frame.hands[0].fingers), 5):
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
				for i in range(len(frame.hands[0].fingers), 5):
					coordinate.append(0.0)
					coordinate.append(0.0)
					coordinate.append(0.0)
		else:
			return

		average = Point(0.0, 0.0)
		for point in frame.pointables:
			point = interactionBox.normalize_point(point.tip_position)
			average.x += point.x
			average.y += point.y

		average.x = average.x / len(frame.pointables)
		average.y = average.y / len(frame.pointables)
		self.printablePoints.append(average)

		self.points.append(coordinate)
		self.printd(len(self.points))
		if Arguments.isSettingAuthentication:
			Storage.write(self.points, "gesture.data")
		return

	def verify(self):
		if Arguments.isUsingPictureMode:
			benchmark = Storage.read("picture.data")

			if len(self.points) != len(benchmark):
				return False
			else:
				for i in range(0, len(benchmark)):
					self.printd(str(abs(self.points[i].x - benchmark[i].x)))
					if abs(self.points[i].x - benchmark[i].x) > Arguments.errorInPicture:
						return False
					elif abs(self.points[i].y - benchmark[i].y) > Arguments.errorInPicture:
						return False
				return True


		elif Arguments.isUsingBinaryMode:
			# May change to another filename
			benchmark = Storage.read("binary.data")
			self.printd("Current: %s" % self.points)
			self.printd("Benchmark: %s" % benchmark)
			return benchmark == self.points

		elif Arguments.isUsingGestureMode:
			benchmark = Storage.read("gesture.data")
			# If numbers of frames have a significant difference, reject immediately.
			if (len(self.points) < len(benchmark) * 0.5) or (len(self.points) > len(benchmark) * 1.5):
				return False
			
			k = Arguments.errorInGesture
			threshold = 0.0
			rmsdiff = 0.0
			for i in range(0, min(len(self.points), len(benchmark))):
				for j in range(0, 30):	
					rmsdiff += (self.points[i][j] - benchmark[i][j]) ** 2
					threshold += k * (benchmark[i][j] ** 2)
			
			rmsdiff += k * abs(len(self.points) - len(benchmark)) * threshold / 20
			rmsdiff = math.sqrt(rmsdiff / min(len(self.points), len(benchmark)))
			threshold = math.sqrt(threshold / min(len(self.points), len(benchmark)))

			self.printd("rmsdiff:")
			self.printd(rmsdiff)
			self.printd("threshold:")
			self.printd(threshold)

			return (rmsdiff <= threshold)

		else:
			return False
			
		

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
				if self.idleCounter >= 30:
					# do verification and display something secret
					Arguments.windowShouldClose = True
					if not Arguments.isSettingAuthentication:
						result = self.verify()
						if result:
							Arguments.isGestureVerified = True
							print "Verification Passed!"
						else:
							Arguments.isGestureVerified = False
							print "Verification Failed!"
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
