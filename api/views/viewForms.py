from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db
from ..util.validator import validate_date_format, validate_integer_text_format

viewforms = Blueprint('viewforms', __name__)

@viewforms.route('/energy_consumption_form/<cust_id>', methods=['GET'])
def getEnergyConsumptionForm(cust_id):
    return render_template("energy_consumption_form.html", cust_id=cust_id)

@viewforms.route('/energy_consumption_per_location/<cust_id>', methods=['GET'])
def getEnergyConsumptionFormPerLocation(cust_id):
    return render_template("energy_consumption_per_location.html", cust_id=cust_id)

@viewforms.route('/comparison_form/<cust_id>', methods=['GET'])
def getComparison(cust_id):
    return render_template("comparison_form.html", cust_id=cust_id)

@viewforms.route('/per_device_consumption/<cust_id>', methods=['GET'])
def getEnergyConsumptionFormPerDevice(cust_id):
    return render_template("per_device_consumption.html", cust_id=cust_id)