import flask
from flask import render_template, request, redirect, url_for,jsonify

dash = flask.Blueprint('dash', __name__)

@dash.route('/Dashboard')
def Dashboard():
    return render_template('DashboardView.html')