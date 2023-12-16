from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db

devices = Blueprint('devices', __name__)

# get devices list with user id
@devices.route("/devices", methods=['GET'])
def getDevicesByUserID():
    result = db.session.execute(text('''Select * 
                                     from device d '''), (cust_id, )).fetchall()
    return result

# add device
@devices.route("/devices", methods=['POST'])
def addDeviceForLocation():
    loc_id = request.form["loc_id"]
    model_id = request.form["model_id"]
    device_id = str(getNextDeviceId())
    db.session.execute(text('''Insert into device (dev_id, loc_id, model_id) values
                       (?,?,?)'''), (device_id, loc_id, model_id, ))
    db.session.commit()
    return {'msg': 'Successfully added'}

# delete device
@devices.route("/devices/<dev_id>", methods=['DELETE'])
def deleteDevice():
    try:
        db.session.execute(text("Delete from device where dev_id=?"), (dev_id,))
        db.session.commit()
        return jsonify({'status': 'error', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextDeviceId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select dev_id from device order by dev_id desc")).fetchone()['dev_id']
    last_db_id_number = int(last_db_id.split("-")[1])
    return 'd-' + str(last_db_id_number+1)