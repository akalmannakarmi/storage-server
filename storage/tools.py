import os,json

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def isAllowed(filename):
	return True
	# return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save(directory,fileTree):
	filePath = os.path.join(directory,"fileTree.json")
	with open(filePath,"w") as f:
		json.dump(fileTree,f,indent=2)
		

def load(directory)->dict:
	filePath = os.path.join(directory,"fileTree.json")
	if not os.path.exists(filePath):
		return {}
	with open(filePath,"r") as f:
		return json.load(f)
		

def getFileTree(directory,update=True):
	dir_dict = {}
	if not update:
		dir_dict = load(directory)
		if dir_dict:
			return dir_dict
		
	for root, dirs, files in os.walk(directory):
		# Create a reference to the current position in the nested dictionary
		path = root.split(os.sep)
		current_level = dir_dict
		
		for part in path:
			current_level = current_level.setdefault(part, {})
		
		# Include all subdirectories
		for dir_name in dirs:
			current_level[dir_name] = {}
		
		# Include files in the current directory
		for file in files:
			current_level[file] = None
	
	save(directory,dir_dict[directory])
	return dir_dict[directory]

def isSafePath(base_path, user_path):
	# Get the absolute path of the base directory
	base_path = os.path.abspath(base_path)
	# Resolve the absolute path of the user-provided path
	user_path = os.path.abspath(os.path.join(base_path, user_path))
	# Check if the user path starts with the base path
	return os.path.commonpath([base_path]) == os.path.commonpath([base_path, user_path])
