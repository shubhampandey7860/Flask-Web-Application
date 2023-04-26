from flask import Blueprint,render_template,request,flash ,redirect,url_for
from .models import User
from . import db   
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)



@auth.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Succesfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password,try again',category='error')   
        else:
            flash('email does not exits',category='error')         
            
        
    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    


@auth.route('/sign-up',methods=['GET',"POST"])
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('fname')
        password1 = request.form.get('pwd1')
        password2 = request.form.get('pwd2')
        
        user = User.query.filter(email=email).first()
        if user:
            flash('email already exits',category='error')
            
        elif len(email) < 4:
            flash('Email must be greater than 4 charters',category='error')
        elif len(name) < 2:
            flash('Name must be greater than 2 charters',category='error')
        elif password1!=password2:
            flash('password does not matched',category='error')
        elif len(password1) < 7:
           flash('Password must be at least 7 charcters ',category='error')
        else:
            new_user = User(email=email,first_name=name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created ',category='success')
            return redirect(url_for('views.home'))
            
            
            
            
            
        
    return render_template('sign_up.html',user=current_user)
