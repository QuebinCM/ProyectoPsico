import flask
from flask import render_template,session
from config import db
from utils.decorators import login_required

dash = flask.Blueprint('dash', __name__)

@dash.route('/Dashboard')
@login_required
def Dashboard():

    user_id = session.get('usuario')

    user_doc = db.collection('usuarios').document(user_id).get()

    user_ref = db.collection('usuarios').document(user_id)

    comprobar_tests = user_ref.collection('tests').limit(1).get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        nombre = user_data['nombre']
        correo=user_data['correo']

        return render_template('DashboardView.html', nombre=nombre, correo=correo, comprobar_tests = comprobar_tests)
    return 'Usuario no encontrado'