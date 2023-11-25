import flask
from flask import render_template

register = flask.Blueprint('register', __name__)

@register.route('/Register')
def Inicio():
    return render_template('RegisterView.html')