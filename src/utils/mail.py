import flask
from flask import redirect, request
import smtplib
from email.mime.text import MIMEText
import os

correo = flask.Blueprint('correo', __name__)

@correo.route('/Correo', methods=['POST'])
def enviar_correo():
    if request.method == 'POST':
        nombre = request.form['nombre_sug']
        correo = request.form['correo_sug']
        mensaje = request.form['mensaje_sug']

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = os.getenv("MAIL")
        smtp_password = os.getenv("PASSWORD")

        # Configurar el mensaje
        msg = MIMEText(f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}")
        msg['Subject'] = "Nuevo mensaje de la caja de sugerencias"
        msg['From'] = smtp_username
        msg['To'] = smtp_username

        try:

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.sendmail(smtp_username, [msg['To']], msg.as_string())

            server.quit()

            return redirect(request.referrer)
        except Exception as e:
            return redirect(request.referrer)