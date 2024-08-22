from flask import render_template,session,request,redirect
from app.wrapers import isUser
from . import app

@app.route('/myFiles',methods=["GET"])
@isUser
def myFiles():
    return render_template('storage/myFiles.html',session=session,current=request.args.get("current",""))

@app.route('/publicFiles',methods=["GET"])
@isUser
def publicFiles():
    return render_template('storage/publicFiles.html',session=session,current=request.args.get("current",""))

@app.route('/myImages',methods=["GET"])
@isUser
def myImages():
    return render_template('storage/myImages.html',session=session,current=request.args.get("current",""))


@app.route('/publicImages',methods=["GET"])
@isUser
def publicImages():
    return render_template('storage/publicImages.html',session=session,current=request.args.get("current",""))

