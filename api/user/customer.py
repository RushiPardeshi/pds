from flask import Blueprint, Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db

customer = Blueprint('customer', __name__)

# get customer with user id
@customer.route("/user/<cust_id>", methods=['GET'])
def getCustomerByUserID():
    result = db.session.execute(text('''Select * 
                                     from customer c  
                                     where c.cust_id = ?'''), (cust_id, )).fetchall()
    return result

# get all locations for a customer
@customer.route("/user/<cust_id>/locations", methods=['GET'])
def getLocationsByUserID():
    result = db.session.execute(text('''Select * 
                                     from service_loc sl  
                                     where sl.cust_id = ?'''), (cust_id, )).fetchall()
    return result

# get devices list with user id
@customer.route("/user/<cust_id>/devices", methods=['GET'])
def getDevicesByUserID():
    result = db.session.execute(text('''Select d.dev_id, m.model_name, m.model_type 
                                     from device d 
                                     natural join service_loc sl 
                                     natural join model m
                                     where sl.cust_id = ? '''), (cust_id, )).fetchall()
    return result

# add user
@customer.route("/user", methods=['POST'])
def addLocation():
    try:
        payload = request.get_json()
        cust_id = getNextCustId()
        addr = payload['addr']
        name = payload['name']
        db.session.execute(text('''Insert into customer(cust_id, name, bill_addr) values 
                                (?,?,?)'''), (cust_id, name, addr, ))
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record added successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# delete user
@customer.route("/user/<cust_id>", methods=['DELETE'])
def deleteDevice():
    try:
        db.session.execute(text("Delete from customer where cust_id=?"), (cust_id,))
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextCustId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select cust_id from customer order by cust_id desc")).fetchone()['cust_id']
    last_db_id_number = int(last_db_id.split("-")[1])
    return 'c-' + str(last_db_id_number+1)