from flask import render_template,session,request,redirect,jsonify,send_from_directory
from . import app
from app.wrapers import isUser
from storage import Storage,isAllowed
import os

@app.route('/upload',methods=["POST"])
@isUser
def upload():
	print("Here")
	if 'file' not in request.files:
		return redirect(request.url)
	
	files = request.files.getlist('file')

	for file in files:
		if file.filename == '':
			continue
		if file and isAllowed(file.filename):
			if not Storage.createPath(session["name"],request.form.get("current",""),file.filename):
				continue
			path = Storage.getPath(session["name"],request.form.get("current",""))
			
			file.save(os.path.join(path, file.filename))

	Storage.updateFileTree()
	return "True"

@app.route('/uploadPublic',methods=["POST"])
@isUser
def uploadPublic():
	if 'file' not in request.files:
		return redirect(request.url)
	files = request.files.getlist('file')

	for file in files:
		if file.filename == '':
			continue
		if file and isAllowed(file.filename):
			if not Storage.createPathPublic(request.form.get("current",""),file.filename):
				continue
			path = Storage.getPathPublic(request.form.get("current",""))

			file.save(os.path.join(path, file.filename))

	Storage.updateFileTree()
	return "True"

@app.route('/download/<filename>',methods=["GET"])
@isUser
def download(filename):
	if Storage.canDownload(session["name"],request.args.get("current",""),filename):
		path = Storage.getPath(session["name"],request.args.get("current",""))
		return send_from_directory(path, filename)
	return "False"


@app.route('/downloadPublic/<filename>',methods=["GET"])
@isUser
def downloadPublic(filename):
	path = Storage.getPathPublic(request.args.get("current",""))
	return send_from_directory(path, filename)