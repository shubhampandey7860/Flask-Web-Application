from flask import Flask 
from  flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
db_Name = "database.db"


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'RADHE KRISHNA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_Name}'
    db.init_app(app)
    
    
    
    
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_preffix='/')
    app.register_blueprint(auth,url_preffix='/')
    
    from .models import  User,Note
    
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app  


def create_database():
    if not path.exists('website/'+ db_Name):
        db.create_all()
        print('created Database') 
      
    
 
    
# with app.app_context(): 
#     if not path.exists('website/'+ db_Name):
#          db.create_all()
#         print('created Database')   
       