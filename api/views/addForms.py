from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db
from ..util.validator import validate_date_format, validate_integer_text_format

addforms = Blueprint('addforms', __name__)

@addforms.route("/add_device_form/<cust_id>", methods=['GET'])
def getAddDeviceForm(cust_id):
    return render_template("add_device_form.html", cust_id=cust_id)

@addforms.route("/add_location_form/<cust_id>", methods=['GET'])
def getAddLocationForm(cust_id):
    return render_template("add_location_form.html", cust_id=cust_id)