from flask import (Flask, g, make_response, render_template, flash, redirect, request, url_for, abort, jsonify)

# Login 
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models

### Basics Application Runnings and Variables 

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


# LOGIN PAGE with Logout Function
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                flash("Logged In", "success")
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

# Logs User Out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Index Page
@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
	return render_template('index.html')








# Run app
if __name__ == '__main__':
	models.initialize()
	try:
		models.User.create_user(
			name='Robbie Peck',
			email='robbie@gmail.com',
			password='FantaDrink123' 
		)
	except ValueError:
		pass
	app.run(debug=DEBUG, host=HOST, port=PORT)
