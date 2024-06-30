import os
from .tools import getFileTree,isAllowed

class Storage:
	@staticmethod
	def init(data_path):
		Storage.dataPath = data_path
		Storage.publicDataPath = os.path.join(Storage.dataPath, "public")
		Storage.privateDataPath = os.path.join(Storage.dataPath, "private")

		os.makedirs(Storage.publicDataPath, exist_ok=True)
		os.makedirs(Storage.privateDataPath, exist_ok=True)

		Storage.fileTree = Storage.updateFileTree()

	@staticmethod
	def createAccount(name):
		os.makedirs(f"{Storage.privateDataPath}/{name}", exist_ok=True)
		Storage.updateFileTree()

	@staticmethod
	def createPath(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, os.path.dirname(fileName))
		else:
			path = os.path.join(Storage.privateDataPath, name, current, os.path.dirname(fileName))
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
		os.makedirs(path, exist_ok=True)

		filePath = os.path.join(Storage.publicDataPath, fileName)
		if os.path.exists(filePath):
			return False

		Storage.updateFileTree()
		return True

	@staticmethod
	def getPath(name, current):
		if current == "":
			return os.path.join(Storage.privateDataPath, name)
		return os.path.join(Storage.privateDataPath,name, current)

	@staticmethod
	def getPathPublic(current):
		if current == "":
			return Storage.publicDataPath
		return os.path.join(Storage.publicDataPath, current)

	@staticmethod
	def canDownload(name, current, fileName):
		if current == "":
			path = os.path.join(Storage.privateDataPath, name, fileName)
		else:
			path = os.path.join(Storage.privateDataPath, name, current, fileName)
		return os.path.exists(path)

	@staticmethod
	def updateFileTree():
		Storage.fileTree = getFileTree(Storage.dataPath)
		return Storage.fileTree