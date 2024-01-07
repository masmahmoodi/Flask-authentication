from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
##CREATE TABLE IN DB

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form["email"]).first():
            flash("you have logged in with this email please log in instead!")
            return redirect(url_for('register'))
        else:
            password = request.form["password"]
            hashed_password = generate_password_hash(password)
            user_info = User(email=request.form["email"],name=request.form["name"],password=hashed_password)
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('secrets', id=user_info.id))
    return render_template("register.html")


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password,request.form["password"] ):
            login_user(user)
            return redirect(url_for('secrets'))

        elif not user:
            flash("This Email does not exist!")
            return redirect(url_for('login'))
        else:
            flash("The password is incorrect !")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html",current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))





@app.route('/download')
def download():
   return send_from_directory(directory="static",filename="files/cheat_sheet.pdf")






if __name__ == "__main__":
    app.run(debug=True)
