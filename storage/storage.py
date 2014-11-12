import pickle

class Storage():
	@staticmethod
	def write(object, filename):
		try:
			with open(filename, 'wb') as writeHandler:
				pickle.dump(object, writeHandler)
		except IOError:
			print "Error writing data, please make sure you have proper permissions!"

	@staticmethod
	def read(filename):
		try: 
			with open(filename, 'rb') as readHandler:
				obj = pickle.load(readHandler)
				return obj
		except IOError:
			print "Please set gesture for authentication first!"