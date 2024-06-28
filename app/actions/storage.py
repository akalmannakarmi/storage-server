from flask import render_template,session,request,redirect,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from . import app
from app.wrapers import isUser
from storage import isAllowed,getPath,getPathPublic,canDownload

@app.route('/upload',methods=["POST"])
@isUser
def upload():
	if 'file' not in request.files:
		return redirect(request.url)
	
	files = request.files.getlist('file')

	for file in files:
		if file.filename == '':
			continue
		if file and isAllowed(file.filename):
			filename = secure_filename(file.filename)

			path = getPath(session["name"],request.form.get("current",""),file.filename)

			file.save(path, filename)

	return render_template('index.html')

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
			filename = secure_filename(file.filename)

			path = getPathPublic(request.form.get("current",""),file.filename)

			file.save(path, filename)

	return render_template('index.html')

@app.route('/download/<filename>',methods=["POST"])
@isUser
def download(filename):
	if canDownload(session["name"],request.form.get("current",""),filename):
		path = getPath(session["name"],request.form.get("current",""),filename)
		return send_from_directory(path, filename)
	return "False"


@app.route('/downloadPublic/<filename>',methods=["POST"])
@isUser
def downloadPublic(filename):
	path = getPathPublic(request.form.get("current",""),filename)
	return send_from_directory(path, filename)