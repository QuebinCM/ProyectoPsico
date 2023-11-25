import flask
from flask import render_template

login = flask.Blueprint('login', __name__)

@login.route('/Login')
def Inicio():
    return render_template('LoginView.html')