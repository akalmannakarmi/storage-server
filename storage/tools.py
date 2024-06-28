import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def isAllowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getFileTree(directory):
    dir_dict = {}
    
    for root, dirs, files in os.walk(directory):
        # Create a reference to the current position in the nested dictionary
        path = root.split(os.sep)
        current_level = dir_dict
        
        for part in path:
            current_level = current_level.setdefault(part, {})
        
        for file in files:
            current_level[file] = None
    
    return dir_dict