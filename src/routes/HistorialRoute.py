import flask
from flask import render_template, session
from config import db

historial = flask.Blueprint('historial', __name__)

preguntas = ['Me enojo por pequeñas cosas',
             'Me siento mareado, como si estuviese a punto de desmayarme',
             'No disfruto nada',
             'Tengo problemas para respirar, a pesar de no hacer esfuerzo o estar enfermo',
             'Odio mi vida',
             'Sobreexagero mis reacciones ante cualquier situación',
             'Mis manos permanecen temblorosas',
             'Estoy estresado por muchas cosas',
             'Me siento con miedo',
             'No hay nada interesante que pueda hacer',
             'Me irrito facilmente',
             'Encuentro difícil relajarme',
             'No puedo dejar de sentirme triste',
             'Me molesta cuando la gente me interrumpe',
             'Siento que estoy a punto de entrar en pánico',
             'Me odio a mi mismo',
             'Siento que no sirvo para nada',
             'Me molesto facilmente',
             'Mi corazón late rápido a pesar de no hacer esfuerzo',
             'Siento miedo sin razón aparente',
             'Siento que mi vida es terrible']
respuestas = []

@historial.route('/Historial/<documento>')
def Historial(documento):
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
            nacimiento = user_data['nacimiento']
            genero = user_data['genero']

            test_doc = db.collection('usuarios').document(user_id).collection('tests').document(documento).get()

            test_data = test_doc.to_dict()

            fecha = test_data['fecha']
            tiempo = test_data['tiempo']
            recomendaciones = test_data['recomendaciones']
            preg_abierta = test_data['pregunta']

            puntajes = test_data['puntajes']
            percentiles = test_data['percentiles']

            respuestas = test_data['resultados']

            datos = {'nacimiento': nacimiento,'genero': genero, 'fecha': fecha, 'tiempo': tiempo, 'recomendaciones': recomendaciones}

    return render_template('HistorialView.html', loged = loged ,nombre=nombre, correo=correo, datos = datos, 
                           puntajes = puntajes, percentiles = percentiles, recomendaciones = recomendaciones, 
                           preg_abierta = preg_abierta, respuestas = respuestas)