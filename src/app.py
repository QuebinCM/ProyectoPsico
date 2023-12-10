from flask import Flask, redirect, url_for, request

from routes.InicioRoute import inicio
from routes.LoginRoute import login
from routes.RegisterRoute import register
from routes.DashboardRoute import dash
from routes.TestRoute import test
from routes.ResultRoute import resultados
from routes.HistorialRoute import historial

from utils.mail import correo

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'grielatest'

app.register_blueprint(inicio)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(dash)
app.register_blueprint(test)
app.register_blueprint(resultados)
app.register_blueprint(correo)
app.register_blueprint(historial)

@app.route('/')
def index():
    return redirect(url_for('inicio.Inicio'))

if __name__ == '__main__':
    app.run(debug=True)