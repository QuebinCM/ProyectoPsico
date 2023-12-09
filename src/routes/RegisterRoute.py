import flask
from flask import render_template, request, redirect,url_for, session, json, flash
from config import auth, db

register = flask.Blueprint('register', __name__)

@register.route('/Register', methods=['GET', 'POST'])
def Inicio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        nacimiento = request.form['nacimiento']
        genero = request.form['genero']
        password = request.form['contra']
        try:
            user = auth.create_user_with_email_and_password(correo, password)
            user_id = user['localId']

            user_data  = {
            'nombre': nombre,
            'nacimiento': nacimiento,
            'genero': genero,
            'correo': correo,
            }

            db.collection('usuarios').document(user_id).set(user_data)

            session['usuario'] = user['localId']

            return redirect(url_for('dash.Dashboard'))
        except Exception as e:
            error_json = e.args[1]
            error_details = json.loads(error_json).get('error', {})
            error_message = error_details.get('message', '')
            print(error_message)

            if error_message == 'EMAIL_EXISTS':
                flash('El correo ya se encuentra en uso.')
            else:
                flash('Error al registrar la cuenta.')

    return render_template('RegisterView.html')