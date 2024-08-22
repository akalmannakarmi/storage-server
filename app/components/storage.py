from flask import render_template,session,request,redirect,make_response
from app.wrapers import isUser
from . import app
from storage import Storage
import os

@app.route('/myFiles',methods=["GET"])
@isUser
def myFiles():
	current=request.args.get('current',"")
	if 'next' in request.args:
		current = os.path.join(current,request.args.get("next"))
	
	folders = current.split(os.sep)
	data = Storage.fileTree["private"][session["name"]]
	pathDict = {}
	current_path = ''
		
	for folder in folders:
		if folder in data:
			data = data[folder]
		current_path = os.path.join(current_path, folder)
		pathDict[folder] = current_path

	response = make_response(render_template('_components/storage/myFiles.html',session=session,current=current,data=data,pathDict=pathDict))
	response.headers['HX-Location'] = f"/myFiles?current={current}"
	return render_template('_components/storage/myFiles.html',session=session,current=current,data=data,pathDict=pathDict)

@app.route('/publicFiles',methods=["GET"])
@isUser
def publicFiles():
	current=request.args.get('current',"")
	if 'next' in request.args:
		current = os.path.join(current,request.args.get("next"))
	
	folders = current.split(os.sep)
	data = Storage.fileTree["public"]
	pathDict = {}
	current_path = ''
		
	for folder in folders:
		if folder in data:
			data = data[folder]
		current_path = os.path.join(current_path, folder)
		pathDict[folder] = current_path

	return render_template('_components/storage/publicFiles.html',session=session,current=current,data=data,pathDict=pathDict)


@app.route('/myImages',methods=["GET"])
@isUser
def myImages():
	image = Storage.getMyImage(session["name"],int(request.args.get("skip",0)),request.args.get("current",""))
	if not image:
		return ""
	image = f"/download/{image}"
	return render_template('_components/storage/myImages.html',session=session,image=image,current=request.args.get("current",""),skip=int(request.args.get("skip",0))+1)


@app.route('/publicImages',methods=["GET"])
@isUser
def publicImages():
	image = Storage.getPublicImage(int(request.args.get("skip",0)),request.args.get("current",""))
	if not image:
		return ""
	image = f"/downloadPublic/{image}"
	return render_template('_components/storage/publicImages.html',session=session,image=image,current=request.args.get("current",""),skip=int(request.args.get("skip",0))+1)

