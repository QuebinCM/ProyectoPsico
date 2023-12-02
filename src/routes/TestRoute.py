import flask
from flask import render_template

test = flask.Blueprint('test', __name__)

@test.route('/Test')
def Inicio():
    return render_template('TestView.html')