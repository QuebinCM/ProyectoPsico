import flask
from flask import render_template, session
from config import db

inicio = flask.Blueprint('inicio', __name__)

@inicio.route('/Inicio')
def Inicio():
    loged = False
    nombre = ''
    correo = ''

    if 'usuario' in session:
        loged = True
        user_id = session['usuario']
        user_doc = db.collection('usuarios').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            nombre = user_data['nombre']
            correo=user_data['correo']

    return render_template('InicioView.html', loged = loged ,nombre=nombre, correo=correo)