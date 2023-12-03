import flask
from flask import render_template, request, redirect,url_for, session
from config import auth, db

register = flask.Blueprint('register', __name__)

@register.route('/Register', methods=['GET', 'POST'])
def Inicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['contra']
        try:
            user = auth.create_user_with_email_and_password(correo, password)
            user_id = user['localId']

            user_data  = {
            'nombre': nombre,
            'correo': correo
            }

            db.collection('usuarios').document(user_id).set(user_data)

            session['usuario'] = user['localId']

            return redirect(url_for('dash.Dashboard'))
        except:
            print('No se puedo crear cuenta')

    return render_template('RegisterView.html')