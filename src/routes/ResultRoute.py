import flask
from flask import redirect, render_template, request, session, url_for
from config import db
from openai import OpenAI
import time
import re
from datetime import datetime, date
from scipy.stats import norm

resultados = flask.Blueprint('resultados', __name__)

client = OpenAI(api_key="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")

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

@resultados.route('/Resultados', methods=['POST', 'GET'])
def Resultados():
    percentil_datos = {
    'primary_school_female_depression': (4.03, 4.74),
    'primary_school_male_depression': (3.88, 4.45),
    'high_school_female_depression': (3.70, 5.10),
    'high_school_male_depression': (2.08, 3.65),
    'primary_school_female_anxiety': (4.02, 4.25),
    'primary_school_male_anxiety': (3.85, 3.89),
    'high_school_female_anxiety': (3.70, 4.61),
    'high_school_male_anxiety': (1.99, 3.15),
    'primary_school_female_stress': (7.61, 4.82),
    'primary_school_male_stress': (7.64, 4.57),
    'high_school_female_stress': (9.31, 5.34),
    'high_school_male_stress': (6.41, 4.74),
    }

    def calcular_percentiles_tres_categorias(puntaje_depresion, puntaje_anxiety, puntaje_stress, grupo, datos):
        percentiles_calcular = {
            'depresion': norm.cdf(puntaje_depresion, *datos[f'{grupo}_depression']),
            'ansiedad': norm.cdf(puntaje_anxiety, *datos[f'{grupo}_anxiety']),
            'estres': norm.cdf(puntaje_stress, *datos[f'{grupo}_stress']),
        }
        print('Estre!!!' + f'{grupo}_stress')
        return {k: int(v * 100) for k, v in percentiles_calcular.items()}

    loged = False
    nombre = ''
    correo = ''
    nacimiento = ''
    genero = ''

    datos = {}
    puntajes = {}

    fecha_actual = datetime.now()

    fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':

        if 'usuario' in session:
            loged = True
            user_id = session['usuario']
            user_doc = db.collection('usuarios').document(user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                nombre = user_data['nombre']
                correo=user_data['correo']
                nacimiento=user_data['nacimiento']
                genero=user_data['genero']

                fecha_nacimiento = datetime.strptime(nacimiento, '%Y-%m-%d')

                actual = datetime.now()

                edad = actual.year - fecha_nacimiento.year - ((actual.month, actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))


                if genero == 'Masculino' and edad < 12:
                    grupo = 'primary_school_male'
                else:
                    grupo = 'high_school_male'

                if genero == 'Femenino' and edad < 12:
                    grupo = 'primary_school_female'
                else:
                    grupo = 'high_school_female'

                datos = {'nacimiento': nacimiento,'genero': genero, 'fecha': fecha_formateada, 'tiempo': request.form['tiempo']}
        else:
            datos = {'nacimiento': request.form['nacimiento'],'genero': request.form['genero'], 'fecha': fecha_formateada, 'tiempo': request.form['tiempo']}

            genero = request.form['genero'],

            fecha_nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d')

            actual = datetime.now()

            edad = actual.year - fecha_nacimiento.year - ((actual.month, actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

            print('Edad: ' + str(edad))
            print('Genero' + str(genero))

            if genero == 'Masculino' and edad < 12:
                grupo = 'primary_school_male'
            elif genero == 'Masculino' and edad >= 12:
                grupo = 'high_school_male'

            if genero == 'Femenino' and edad < 12:
                grupo = 'primary_school_female'
            elif genero == 'Femenino' and edad >= 12:
                grupo = 'high_school_female'

        rutina_text = request.form['rutina_text']
        preguntas_depresion = [3, 5, 10, 13, 16, 17, 21]
        preguntas_ansiedad = [2, 4, 7, 9, 15, 19, 20]
        preguntas_estres = [1, 6, 8, 11, 12, 14, 18]

        suma_depresion = 0
        suma_ansiedad = 0
        suma_estres = 0

        def sumar_categoria(preguntas):
            suma = 0
            for num_pregunta in preguntas:
                valor = request.form.get(f'preg-{num_pregunta}')
                if valor is not None:
                    suma += int(valor)
            return suma
        
        suma_depresion = sumar_categoria(preguntas_depresion)
        suma_ansiedad = sumar_categoria(preguntas_ansiedad)
        suma_estres = sumar_categoria(preguntas_estres)

        print(suma_ansiedad)
        print(suma_depresion)
        print(suma_estres)

        total = int(suma_depresion) + int(suma_ansiedad) + int(suma_estres)

        puntajes = {'depresion': suma_depresion, 'ansiedad': suma_ansiedad, 'estres': suma_estres, 'total': total}


        percentiles_grupo = calcular_percentiles_tres_categorias(
            int(suma_depresion), 
            int(suma_ansiedad), 
            int(suma_estres),
            grupo, 
            percentil_datos
        )

        message_thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": "Tengo ansiedad de nivel "+str(suma_ansiedad)+", tengo estres nivel "+str(suma_estres)+", tengo depresión nivel "+str(suma_depresion)+", dame recomendaciones y consejos basados en los resultados arrojados por el formulario y en lo que hice la última semana: "+rutina_text
            },
        ]
        )
        thread_id_interno=message_thread.id
        print(message_thread)
        print(thread_id_interno)

        thread_message = client.beta.threads.messages.create(
        thread_id_interno,
        role="user",
        content="Tengo ansiedad de nivel "+str(suma_ansiedad)+", tengo estres nivel "+str(suma_estres)+", tengo depresión nivel "+str(suma_depresion)+", dame recomendaciones y consejos basados en los resultados arrojados por el formulario y en lo que hice la última semana: "+rutina_text,
        )
        print(thread_message)
        print(thread_message.id)
        message_thread_id=thread_message.id


        run = client.beta.threads.runs.create(
        thread_id=thread_id_interno,
        assistant_id="asst_MNbQa1tvLUw2xVdkpJaecDOR",
        instructions="Tengo ansiedad de nivel "+str(suma_ansiedad)+", tengo estres nivel "+str(suma_estres)+", tengo depresión nivel"+str(suma_depresion)+", dame recomendaciones y consejos basados en los resultados arrojados por el formulario y en lo que hice la última semana: "+rutina_text
        )
        print(run)

        time.sleep(30)
        messages = client.beta.threads.messages.list(
        thread_id=thread_id_interno,
        )
        print(messages)

        print(message_thread)

        my_thread = client.beta.threads.messages.list(thread_id_interno)
        print(my_thread.data)
        texto=my_thread.data
        resultados = re.findall(r"value='(.*?)'", str(texto), re.DOTALL)
        for i, resultado in enumerate(resultados, start=1):
            print(f"Texto {i}:\n{resultado}\n")

        print(resultados[0])

        respuestas.clear()
        for i in range(1, 22):
            pregunta = f'preg-{i}'
            respuesta = request.form.get(pregunta)
            respuestas.append((preguntas[i-1], respuesta))
        
        print(respuestas)
        
        # Guardar en la base de datos

        if 'usuario' in session:
            user_id = session['usuario']

            datos_resultados = {pregunta: respuesta for pregunta, respuesta in respuestas}

            guardar = db.collection('usuarios').document(user_id).collection('tests').add({
                'pregunta': rutina_text,
                'recomendaciones': resultados[0],
                'fecha' :fecha_formateada,
                'tiempo': request.form['tiempo'],
                'resultados': datos_resultados,
                'puntajes': puntajes,
                'percentiles': percentiles_grupo,
                'fecha_creacion': datetime.now()
            })

        return render_template('ResultView.html', respuestas=respuestas, texto=resultados[0], 
                               loged = loged, nombre = nombre, correo = correo ,datos = datos, 
                               preg_abierta = rutina_text, puntajes = puntajes, percentiles = percentiles_grupo)
    else:
        return redirect(url_for('inicio.Inicio'))