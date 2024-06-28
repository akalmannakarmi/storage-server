import os
from .tools import getFileTree,isAllowed

dataPath=""
publicDataPath=""
privateDataPath=""

fileTree = {}

def init(data_path):
	global dataPath,publicDataPath,privateDataPath,fileTree
	dataPath = data_path
	publicDataPath=os.path.join(dataPath,"public")
	privateDataPath=os.path.join(dataPath,"private")

	os.makedirs(publicDataPath,exist_ok=True)
	os.makedirs(privateDataPath,exist_ok=True)

	fileTree=tools.getFileTree(dataPath)

def createAccount(name):
	os.makedirs(f"{privateDataPath}/{name}",exist_ok=True)

def createPath(name,current,fileName):
	if current=="":
		path = os.path.join(privateDataPath,name,os.path.dirname(fileName))
	else:
		path = os.path.join(privateDataPath,name,current,os.path.dirname(fileName))
	os.makedirs(path,exist_ok=True)

	filePath = os.path.join(privateDataPath,name,fileName)
	if os.path.exists(filePath):
		return False

	updateFileTree()

def getPath(name,current):
	if current=="":
		return os.path.join(privateDataPath,name)
	return os.path.join(privateDataPath,current,name)

def getPathPublic(current):
	if current=="":
		return publicDataPath
	return os.path.join(publicDataPath,current)

def canDownload(name,current,fileName):
	if current=="":
		path = os.path.join(privateDataPath,name,fileName)
	else:
		path = os.path.join(privateDataPath,name,current,fileName)
	if os.path.exists(path):
		return True
	return False

def updateFileTree():
	global fileTree,dataPath
	fileTree=tools.getFileTree(dataPath)
