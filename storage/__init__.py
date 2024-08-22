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
			return False
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
			return False
		
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
			return False
		
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
			return Storage.privateDataPath
		return path

	@staticmethod
	def getPathPublic(current):
		if current == "":
			path= Storage.publicDataPath
		else:
			path= os.path.join(Storage.publicDataPath, current)
		if not isSafePath(Storage.publicDataPath,path):
			return Storage.publicDataPath
		return path

	@staticmethod
	def canDownload(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, fileName)
		else:
			path = os.path.join(Storage.privateDataPath, name, current, fileName)
		
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			return False
		return os.path.exists(path)
	
	@staticmethod
	def canDownloadPublic(current, fileName):
		if current == "":
			path = os.path.join(Storage.publicDataPath, fileName)
		else:
			path = os.path.join(Storage.publicDataPath, current, fileName)
		
		if not isSafePath(Storage.publicDataPath,path):
			return False
		return os.path.exists(path)	

	@staticmethod
	def delete(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, fileName)
		else:
			path = os.path.join(Storage.privateDataPath, name, current, fileName)
		
		if not isSafePath(os.path.join(Storage.privateDataPath, name),path):
			return False
		if os.path.isfile(path):
			os.remove(path)
			Storage.updateFileTree()
			return True
		return False

	@staticmethod
	def updateFileTree(update=True):
		Storage.fileTree = getFileTree(Storage.dataPath,update)
		return Storage.fileTree