from flask import Flask, redirect, url_for

from routes.InicioRoute import inicio
from routes.LoginRoute import login
from routes.RegisterRoute import register
from routes.DashboardRoute import dash
from routes.TestRoute import test

app = Flask(__name__, static_url_path='/static')

app.register_blueprint(inicio)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(dash)
app.register_blueprint(test)

@app.route('/')
def index():
    return redirect(url_for('inicio.Inicio'))

if __name__ == '__main__':
    app.run(debug=True)