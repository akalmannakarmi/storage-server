from flask import render_template,session,request,redirect,make_response
from app.wrapers import isUser
from . import app
from storage import fileTree
import os

@app.route('/myFiles',methods=["GET"])
@isUser
def myFiles():
	current=request.args.get('current',"")
	if 'next' in request.args:
		current = os.path.join(current,request.args.get("next"))
	folders = current.split(os.sep)
	data = fileTree["private"][session["name"]]
	pathDict = {}
	current_path = ''
		
	for folder in folders:
		if folder in data:
			data = data[folder]
		current_path = os.path.join(current_path, folder)
		pathDict[folder] = current_path

	response = make_response(render_template('_components/storage/myFiles.html',session=session,current=current,data=data,pathDict=pathDict))
	response.headers['HX-Location'] = f"/myFiles?current={current}"
	return response

@app.route('/publicFiles',methods=["GET"])
@isUser
def publicFiles():
	current=request.args.get('current',"")
	if 'next' in request.args:
		current = os.path.join(current,request.args.get("next"))
	folders = current.split(os.sep)
	data = fileTree["private"]
	pathDict = {}
	current_path = ''
		
	for folder in folders:
		if folder in data:
			data = data[folder]
		current_path = os.path.join(current_path, folder)
		pathDict[folder] = current_path

	response = make_response(render_template('_components/storage/publicFiles.html',session=session,current=current,data=data,pathDict=pathDict))
	response.headers['HX-Location'] = f"/publicFiles?current={current}"
	return response