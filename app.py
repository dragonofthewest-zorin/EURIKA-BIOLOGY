from flask import Flask, flash, redirect, render_template, request, Response, url_for, session
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , login_user, logout_user, current_user , login_required
from flask_bcrypt import Bcrypt




db = SQLAlchemy()

from models import User


def create_app():
    global app, login_manager, bcrypt
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/",
    )

    app.secret_key = "no one knows"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mydb.db'

    login_manager = LoginManager()
    bcrypt = Bcrypt(app)


    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    @app.route("/")
    def index():
     return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            form = request.form
            if form:
                username = form.get("username")
                password = form.get("password")
                user = User.query.filter_by(username=username).first()
                if user and bcrypt.check_password_hash(user.password, password):
                        login_user(user)
                        return render_template("login_success.html", id=id)
                else:
                 flash("Invalid username or password")
                 return render_template("login.html", id=id)
               
        
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
        return render_template("login.html", id=id)
        
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))


    @app.route('/upload', methods=['GET','POST'])
    def upload():
     if request.method=='GET':
      return render_template('uploads.html')
     elif request.method=='POST':
      file = request.files.get('file')
      if not file or not file.filename:
         return "No file selected"
      if file.content_type == 'application/pdf':
         return file.read(), 200, {'Content-Type': file.content_type}
      elif file.content_type in ('application/msword',
                                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
         df = pd.read_word(file)
         return df == pd.read_word(file)   
      else:
         return "Unsupported file type"

    @app.route('/Anatomy', methods=['GET', 'POST'])
    def ANATOMY():
     if request.method == 'GET':
        return render_template('anatomy.html')
     elif request.method=='POST':
      organ_system = request.form.get('Organ_System', '').strip()


      if organ_system in (
    'Digestive System',
    'Respiratory System',
    'Circulatory System',
    'Nervous System',
    'Muscular System',
    'Skeletal System',
    'Endocrine System',   
    'Urinary System',
    'Reproductive System',
    'Integumentary System',
      ):
         return learn_about(organ_system)
      else: 

         return "No Organ System Selected"


    @app.route('/Anatomy/<Organ_System>') 
    def learn_about(Organ_System):
     if Organ_System == 'Digestive System':
      return render_template ('Digestive System.html')
     else:

      return f"Explore the {Organ_System} of the Human Body"
     



    @app.route('/users')
    @login_required
    def get_users():
          if current_user.is_authenticated:
           All_users = User.query.all()
           return render_template('users.html', ALL_users=All_users)
          else:
             return "only authenticated users can access this page"

    @app.route("/add_user", methods=["GET", "POST"])
    def add_user():
     if request.method == "GET":
         return render_template("addnewuser.html")
     if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        age = request.form.get("age")
        education_level = request.form.get("education_level")

        
       
        if not username or not password:
            return "Username and password are required."
            return redirect(url_for("add_user"))

        
        if User.query.filter_by(username=username).first():
            return "That username is already taken."
            return redirect(url_for("add_user"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=hashed_pw,
                        age=age, education_level=education_level)
        db.session.add(new_user)
        db.session.commit()
        return render_template("user_added.html")

    
     return render_template("addnewuser.html")

    @app.route('/delete_user/<id>', methods=['DELETE'])
    def delete_user(id):
         all_users = User.query.all()
         user = User.query.filter_by(id=id).first()
         if user:
             db.session.delete(user)
             db.session.commit()

         all_users = User.query.all()
         return render_template('users.html', ALL_users=all_users)

    @app.route('/details/<id>')
    def show_user_details(id):
        all_users = User.query.all()
        user = User.query.get(id)
        if user:
            return render_template('detail.html', ALL_users=all_users, user=user)
        else:
            return "User not found"



    return app  