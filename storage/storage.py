import pickle

class storage():
	@staticmethod
	def write(object, filename):
		with open(filename, 'wb') as writeHandler:
			pickle.dump(object, writeHandler)

	@staticmethod
	def read(filename):
		with open(filename, 'rb') as readHandler:
			obj = pickle.load(readHandler)
			return obj