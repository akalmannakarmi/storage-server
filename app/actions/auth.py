from flask import render_template,session,request,redirect,jsonify
from . import app
from app import db
from app.models import User
from app.wrapers import isUser,isNotUser
import bcrypt

@app.route('/login',methods=["POST"])
@isNotUser
def login():
	data = request.form.deepcopy()
	rq=['name','password']
	if any(i not in data for i in rq):
		result = {"Require":{','.join(rq)}}
		return jsonify(result)

	user = User.query.filter_by(name=data['name']).first()
	if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
		session['userId']=user.id
		session['name']=user.name
		return redirect(request.form.get("next",'/'))
	
	return redirect('/login?error=Incorrect name or password')

@app.route('/signUp',methods=["POST"])
@isNotUser
def signUp():
	data = request.form.deepcopy()
	
	rq=['name','password']
	if any(i not in data for i in rq):
		result = {"Require":{','.join(rq)}}
		return jsonify(result)
		
	if len(data['name']) > 64:
		return redirect('/signUp?error=name too long')

	hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
	new_user = User(name=data['name'],password=hashed_password,kind="user")
	db.session.add(new_user)
	db.session.commit()

	return redirect(request.form.get("next",'/login'))

@app.route('/logout',methods=["GET","POST"])
@isUser
def logout():
    session.clear()
    return redirect('/')