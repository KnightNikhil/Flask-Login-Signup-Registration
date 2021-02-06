from flask import Flask, session, url_for, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'



class users(db.Model):
    _id = db.Column('id', db.Integer , primary_key= True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

@app.route("/")
@app.route("/home")
def homepage():
    if "email" in session:
        first_name= session["first_name"]
        last_name = session["last_name"]
        return f"Hello {first_name} {last_name}"
    else:
        return "Welcome, Please Login to continue!!"
    
@app.route('/show_all')
def show_all():
    if "email" in session:
        return render_template('show_all.html', users = users.query.all() )
    else:
        return "Welcome, Please Login to continue!!"

@app.route('/register', methods = ['GET', 'POST'])
def signuppage():
   if request.method == 'POST':
      if not request.form['first_name'] or not request.form['last_name'] or not request.form['email'] or not request.form['password'] or not request.form['cnf_password']:
         flash('Please enter all the fields', 'error')
      else:
        if request.form['password'] == request.form['cnf_password']:
           user = users(request.form['first_name'],request.form['last_name'], request.form['email'],request.form['password'])  
           db.session.add(user)
           db.session.commit()
           flash('Record was successfully added')
           return redirect(url_for('loginpage'))
        else:   
             flash("Passwords don't match")
             return render_template('show_all.html')
   return render_template('registration.html')

@app.route('/login', methods = ["POST", "GET"])
def loginpage():
    if request.method== "POST":
        if not request.form['email'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            email = request.form["email"]
            password = request.form["password"]
            found_user = users.query.filter_by(email= email).first() 
            if found_user.password == password:
                session["first_name"] = found_user.first_name
                session["last_name"] = found_user.last_name
                session["email"] = found_user.email
                session["password"] = found_user.password
                return redirect(url_for('homepage'))
            else:
                flash("Incorrect id or password")
                return redirect(url_for('loginpage'))
    return render_template('newlogin.html')

@app.route('/logout')
def logoutpage():
    if "email" in session:
        session.pop("email", None)
        session.pop("first_name", None)
        session.pop("last_name", None)
        session.pop("password", None)
        flash("You have been successfully logged out!!")
        return redirect(url_for('loginpage'))
    else:
        flash("You are not logged in!!")
        return redirect(url_for('loginpage'))






if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
