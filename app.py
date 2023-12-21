from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from api.devices.devices import devices
from api.serviceLocations.serviceLocation import serviceLocation
from api.user.customer import customer
from api.util.validator import validate_date_format, validate_integer_text_format
from api.views.view import view
from api.views.viewForms import viewforms
from api.views.addForms import addforms
from db import init_app, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:animefreak@localhost/project'
app.register_blueprint(devices)
app.register_blueprint(serviceLocation)
app.register_blueprint(customer)
app.register_blueprint(view)
app.register_blueprint(viewforms)
app.register_blueprint(addforms)
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/logout')
def logout():
    print(url_for('login'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
