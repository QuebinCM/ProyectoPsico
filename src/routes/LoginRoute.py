import flask
from flask import render_template, request, url_for, redirect, session, json, flash
from config import auth

login = flask.Blueprint('login', __name__)

@login.route('/Login', methods=['GET', 'POST'])
def Inicio():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contra']
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            session['usuario'] = user['localId']

            return redirect(url_for('dash.Dashboard'))
        except Exception as e:
            error_json = e.args[1]
            error_details = json.loads(error_json).get('error', {})
            error_message = error_details.get('message', '')
            print(error_message)

            if error_message == 'INVALID_LOGIN_CREDENTIALS':
                flash('Correo o contraseña incorrectos. Intente de nuevo.')
            else:
                flash('Error al iniciar sesión.')

    return render_template('LoginView.html')

@login.route('/Logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('inicio.Inicio'))