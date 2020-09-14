from flask import request, jsonify, redirect, url_for, render_template, make_response, current_app
from .models import User, Blacklist
from .forms import UserForm
from app.auth.forms import LoginForm
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required, set_access_cookies, jwt_refresh_token_required, create_refresh_token, get_raw_jwt,get_jti,get_jwt_claims
import bcrypt
from datetime import datetime, timedelta
import requests
from app import AppFlask
from app.decorators.unauthorized import admin_required

from . import auth

jwt = AppFlask.get_instance_jwt()

def create_hash(password):
    salt = bcrypt.gensalt(12)
    password = bcrypt.hashpw(password.encode(),salt).decode()
    return password

def checkpw(password_saved,password_by_testing):
    return bcrypt.checkpw(password_by_testing.encode(),password_saved.encode())

def save_tokens_to_blacklist(access_token,refresh_token):
    jti_access = get_jti(encoded_token=access_token)
    jti_refresh = get_jti(encoded_token=refresh_token)
    jwt_token = Blacklist('jwt',jti_access,False,datetime.utcnow())
    refresh_token = Blacklist('refresh',jti_refresh,False,datetime.utcnow())
    jwt_token.save()
    refresh_token.save()
    print('saved tokens to after check')

@jwt.user_claims_loader
def add_claims_to_user_token(identity):
    privilegies = User.get_role(identity)
    current_app.logger.info(privilegies)
    return {'is_admin': privilegies}

@auth.route('/register_user/',methods=['POST','GET'])                                
def register_user():                        
    form = UserForm()     
    if form.validate_on_submit():
        password = create_hash(form.password.data)
        n_user = User(form.username.data,password,form.email.data)
        n_user.save()                     
        return redirect(url_for('public.index'))
    else:
        return render_template('auth/user_form.html', form=form)

@auth.route('/get_user/<int:id>/')
def get_user(id):
    user = User.query.get(id)
    return jsonify({"username":user.username,"password":user.password,"email":user.email})                                          

@auth.route('/get_users/')
def get_users():
    users = [(user.username,user.password, user.email) for user in User.query.all()]
    return jsonify(users)

@auth.route('/update_user/<int:id>',methods=['PATCH'])                                 
def update_user(id):                
    user = User.query.get(id)         
    user.username = request.json['username']
    user.email = request.json['email']
    try:
        db.session.commit()
        return jsonify({"message":"success operation"}), 204
    except:
        return jsonify({"message":"An error detected"})

@auth.route('/update_user_pass/',methods=['POST'])
def update_user_pass():
    id_= request.form['id']               
    user = User.query.get(id_)
    password = PassHash(request.form['password'])
    password = password.create_hash()['token']                                        
    user.update_user_pass(password)        
    return redirect(url_for('public.index'))

@auth.route('/delete_user/<int:id>/',methods=['DELETE'])                             
def delete_user(id):                     
    user = User.query.get(id)          
    db.session.delete(user)          
    db.session.commit()                   
    return jsonify({"message":"user was deleted"})

@auth.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
    
        if username is not None and bcrypt.checkpw(form.password.data.encode(),username.password.encode()):
            access_token = create_access_token(identity=username.username)
            fresh_token = create_refresh_token(identity=username.username)

            save_tokens_to_blacklist(access_token,fresh_token)

            resp = make_response(redirect(url_for('public.index')))
            resp.set_cookie('access_token',access_token,max_age=timedelta(minutes=10))
            resp.set_cookie('refresh_token_cookie',fresh_token,max_age=timedelta(minutes=30))
            return resp
        else:
            print('username or password is wrong')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/login_form.html',form=form)


@auth.route('/logout/')
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    refresh_jti = Blacklist.query.get(jti)
    refresh_jti.update_state()
    resp = make_response(redirect(url_for('auth.logout2')))
    resp.set_cookie('access_token','',max_age=0)
    return resp

@auth.route('/refresh_token/')
@jwt_refresh_token_required
def refresh():
    if User.query.filter_by(username=get_jwt_identity()) is not None:
        access_token = create_access_token(identity = get_jwt_identity())
        resp = make_response(redirect(url_for('public.index')))
        resp.set_cookie('access_token',access_token)
        return resp

@auth.route('/logout2')
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    user = get_raw_jwt()['identity']
    refresh_jti = Blacklist.query.get(jti)
    refresh_jti.update_state()
    resp = make_response(redirect(url_for('public.index')))    
    resp.set_cookie('refresh_token_cookie','',max_age=0)                      
    print(f'user {user} realized logout')
    return resp


@auth.route('/protected/')
@jwt_required
@admin_required
def protec():
    username = get_jwt_identity()
    userinfo = get_jwt_claims()
    print(userinfo)
    return str(username)


