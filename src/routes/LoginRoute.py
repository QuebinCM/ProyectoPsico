import flask
from flask import render_template, request, url_for, redirect, session
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
        except:
            print('No se puedo entrar')

    return render_template('LoginView.html')

@login.route('/Logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('inicio.Inicio'))