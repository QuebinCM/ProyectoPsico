import flask
from flask import render_template, session, request
from config import db
from openai import OpenAI
import time
import re

test = flask.Blueprint('test', __name__)
client = OpenAI(api_key="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")

@test.route('/Test')
def Test():
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

    return render_template('TestView.html', loged = loged ,nombre=nombre, correo=correo)

@test.route('/actualizar', methods=['POST'])
def actualizar():
    
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
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaFINAL\n")
    messages = client.beta.threads.messages.list(
    thread_id=thread_id_interno,
    )
    print(messages)
    print("sdadasdfafa\n")
    print(message_thread)

    my_thread = client.beta.threads.messages.list(thread_id_interno)
    print(my_thread.data)
    texto=my_thread.data
    resultados = re.findall(r"value='(.*?)'", str(texto), re.DOTALL)
    for i, resultado in enumerate(resultados, start=1):
        print(f"Texto {i}:\n{resultado}\n")

    print(resultados[0])
    print("sdadasdfaffsd33333a\n")

    return render_template('TestView.html', texto=resultados[0])