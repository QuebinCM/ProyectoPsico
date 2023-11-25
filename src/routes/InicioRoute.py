import flask
from flask import render_template, request, redirect, url_for,jsonify

inicio = flask.Blueprint('inicio', __name__)

@inicio.route('/Inicio')
def Inicio():
    return render_template('InicioView.html')