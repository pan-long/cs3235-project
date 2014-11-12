from PIL import Image, ImageTk

class Arguments():
	isSettingAuthentication = False
	isUsingBinaryMode = False
	isUsingGestureMode = False
	isUsingPictureMode = False
	isUsingDebugMode = False
	picturePath = ""
	image = None

	errorInGesture = 0.10
	errorInPicture = 0.10
	depthForPictureMode = -0.25
	depthForBinaryMode = 0

	windowShouldClose = False
	isGestureVerified = False