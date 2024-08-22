import os
from .tools import getFileTree,isAllowed,isSafePath

class Storage:
	@staticmethod
	def init(data_path):
		Storage.dataPath = data_path
		Storage.publicDataPath = os.path.join(Storage.dataPath, "public")
		Storage.privateDataPath = os.path.join(Storage.dataPath, "private")

		os.makedirs(Storage.publicDataPath, exist_ok=True)
		os.makedirs(Storage.privateDataPath, exist_ok=True)

		Storage.fileTree = Storage.updateFileTree(False)

	@staticmethod
	def createAccount(name):
		path=os.path.join(Storage.privateDataPath, name)
		if not isSafePath(Storage.privateDataPath,path):
			raise BaseException("Not Safe Path")
		os.makedirs(path, exist_ok=True)
		Storage.updateFileTree()
		return True

	@staticmethod
	def createPath(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, os.path.dirname(fileName))
		else:
			path = os.path.join(Storage.privateDataPath, name, current, os.path.dirname(fileName))
		
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			raise BaseException("Not Safe Path")
		
		os.makedirs(path, exist_ok=True)

		filePath = os.path.join(Storage.privateDataPath, name, fileName)
		if os.path.exists(filePath):
			return False

		Storage.updateFileTree()
		return True
		
	@staticmethod
	def createPathPublic(current, fileName):
		if current == "":
			path = os.path.join(Storage.publicDataPath, os.path.dirname(fileName))
		else:
			path = os.path.join(Storage.publicDataPath, current, os.path.dirname(fileName))
		
		if not isSafePath(Storage.publicDataPath,path):
			raise BaseException("Not Safe Path")
		
		os.makedirs(path, exist_ok=True)

		filePath = os.path.join(Storage.publicDataPath, fileName)
		if os.path.exists(filePath):
			return False

		Storage.updateFileTree()
		return True

	@staticmethod
	def getPath(name, current):
		if current == "":
			path= os.path.join(Storage.privateDataPath, name)
		else:
			path= os.path.join(Storage.privateDataPath,name, current)
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			raise BaseException("Not Safe Path")
		return path

	@staticmethod
	def getPathPublic(current):
		if current == "":
			path= Storage.publicDataPath
		else:
			path= os.path.join(Storage.publicDataPath, current)
		if not isSafePath(Storage.publicDataPath,path):
			raise BaseException("Not Safe Path")
		return path

	@staticmethod
	def canDownload(name, current, fileName):
		print(f"Here {fileName}")
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, fileName)
		else:
			path = os.path.join(Storage.privateDataPath, name, current, fileName)
		
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			raise BaseException("Not Safe Path")
		return os.path.exists(path)
	
	@staticmethod
	def canDownloadPublic(current, fileName):
		if current == "":
			path = os.path.join(Storage.publicDataPath, fileName)
		else:
			path = os.path.join(Storage.publicDataPath, current, fileName)
		
		if not isSafePath(Storage.publicDataPath,path):
			raise BaseException("Not Safe Path")
		return os.path.exists(path)	

	@staticmethod
	def delete(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, fileName)
		else:
			path = os.path.join(Storage.privateDataPath, name, current, fileName)
		
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			raise BaseException("Not Safe Path")
		if os.path.isfile(path):
			os.remove(path)
			Storage.updateFileTree()
			return True
		return False

	@staticmethod
	def updateFileTree(update=True):
		Storage.fileTree = getFileTree(Storage.dataPath,update)
		return Storage.fileTree
	
	@staticmethod
	def getMyImage(name,skip,current=""):
		extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico")
		folders = current.split(os.sep)
		count = 0
		nth_image = None
		
		def traverse_dict(d,back):
			nonlocal count, nth_image, extensions
			for key, value in d.items():
				if isinstance(value, dict):
					if traverse_dict(value,[*back,key]):
						return True # Stop found in nested traversal
				else:
					if key.lower().endswith(extensions):
						if count == skip:
							nth_image = ""
							for b in back:
								nth_image = os.path.join(nth_image,b)
							nth_image = os.path.join(nth_image,key)
							return True  # Stop further traversal
						count += 1
			return False  # Continue traversal if nth image is not found

		d = Storage.fileTree["private"][name]
		for folder in folders:
			if folder in d:
				d = d[folder]
		traverse_dict(d,[])
		return nth_image
	
	@staticmethod
	def getPublicImage(skip,current=""):
		extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico")
		folders = current.split(os.sep)
		count = 0
		nth_image = None
		
		def traverse_dict(d,back):
			nonlocal count, nth_image, extensions
			for key, value in d.items():
				if isinstance(value, dict):
					if traverse_dict(value,[*back,key]):
						return True # Stop found in nested traversal
				else:
					if key.lower().endswith(extensions):
						if count == skip:
							nth_image = ""
							for b in back:
								nth_image = os.path.join(nth_image,b)
							nth_image = os.path.join(nth_image,key)
							return True  # Stop further traversal
						count += 1
			return False  # Continue traversal if nth image is not found

		d = Storage.fileTree["public"]
		for folder in folders:
			if folder in d:
				d = d[folder]
		traverse_dict(d,[])
		return nth_image
	