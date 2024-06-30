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
	fails = []
	for file in files:
		if file.filename == '':
			fails.append("Empty filename!")
			continue
		if file and isAllowed(file.filename):
			if not Storage.createPath(session["name"],request.form.get("current",""),file.filename):
				fails.append(f"{file.filename} Already Exists!")
				continue
			path = Storage.getPath(session["name"],request.form.get("current",""))
			
			file.save(os.path.join(path, file.filename))
	
	Storage.updateFileTree()
	if fails:
		result = f"Failed: {' '.join(fails)}"
		return render_template("/basic/warn.html",msg=result)
	return render_template("/basic/success.html",msg="Successfully Uploaded")

@app.route('/uploadPublic',methods=["POST"])
@isUser
def uploadPublic():
	if 'file' not in request.files:
		return redirect(request.url)
	
	files = request.files.getlist('file')
	fails = []
	for file in files:
		if file.filename == '':
			fails.append("Empty filename!")
			continue
		if file and isAllowed(file.filename):
			if not Storage.createPathPublic(request.form.get("current",""),file.filename):
				fails.append(f"{file.filename} Already Exists!")
				continue
			path = Storage.getPathPublic(request.form.get("current",""))

			file.save(os.path.join(path, file.filename))

	Storage.updateFileTree()
	if fails:
		result = f"Failed: {' '.join(fails)}"
		return render_template("/basic/warn.html",msg=result)
	return render_template("/basic/success.html",msg="Successfully Uploaded")

@app.route('/download/<filename>',methods=["GET"])
@isUser
def download(filename):
	if Storage.canDownload(session["name"],request.args.get("current",""),filename):
		path = Storage.getPath(session["name"],request.args.get("current",""))
		return send_from_directory(path, filename, as_attachment=True)
	return render_template("/basic/warn.html",msg="You can not Download the file")


@app.route('/downloadPublic/<filename>',methods=["GET"])
@isUser
def downloadPublic(filename):
	if Storage.canDownloadPublic(request.args.get("current",""),filename):
		path = Storage.getPathPublic(request.args.get("current",""))
		return send_from_directory(path, filename, as_attachment=True)
	return render_template("/basic/warn.html",msg="You can not Download the file")