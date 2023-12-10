import flask
from flask import render_template,session
from config import db
from firebase_admin import firestore
from utils.decorators import login_required

dash = flask.Blueprint('dash', __name__)

@dash.route('/Dashboard')
@login_required
def Dashboard():

    datos = {}
    documentos_tests= {}
    puntajes = {}
    percentiles = {}

    user_id = session.get('usuario')

    user_doc = db.collection('usuarios').document(user_id).get()

    user_ref = db.collection('usuarios').document(user_id)

    if user_doc.exists:
        user_data = user_doc.to_dict()
        comprobar_tests = user_ref.collection('tests').limit(1).get()

        nombre = user_data['nombre']
        correo=user_data['correo']
        nacimiento=user_data['nacimiento']
        genero=user_data['genero']

        if comprobar_tests:
            test_ref = (
            user_ref
            .collection('tests')
            .order_by('fecha_creacion', direction=firestore.Query.DESCENDING)
            .limit(1)
            )

            ultimo_test = next(test_ref.stream(), None)

            datos_ultimo_test = ultimo_test.to_dict()

            fecha = datos_ultimo_test['fecha']
            tiempo = datos_ultimo_test['tiempo']
            recomendaciones = datos_ultimo_test['recomendaciones']

            puntajes = datos_ultimo_test['puntajes']
            percentiles = datos_ultimo_test['percentiles']

            datos = {'nacimiento': nacimiento,'genero': genero, 'fecha': fecha, 'tiempo': tiempo, 'recomendaciones': recomendaciones}

            tests_ref = (
                user_ref
                .collection('tests')
                .stream()
            )

            documentos_tests = [{'id': test.id, **test.to_dict()} for test in tests_ref]

        return render_template('DashboardView.html', nombre=nombre, correo=correo, comprobar_tests = comprobar_tests, datos = datos, documentos_tests = documentos_tests, 
                               puntajes = puntajes, percentiles = percentiles)
    return 'Usuario no encontrado'