from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
from db import db
from ..util.validator import validate_integer_text_format

devices = Blueprint('devices', __name__)

# get devices list with user id
# @devices.route("/devices", methods=['GET'])
# def getDevicesByUserID():
#     result = db.session.execute(text('''Select * from device d''')).fetchall()
#     return result

@devices.route("/models", methods=['GET'])
def getModels():
    result = db.session.execute(text('''select * from model''')).fetchall()
    results = []
    for r in result:
        dic = {}
        dic['model_id'] = r[0]
        dic['model_name'] = r[1]
        dic['model_type'] = r[2]
        results.append(dic)
    return results


# add device
@devices.route("/devices", methods=['POST'])
def addDeviceForLocation():
    payload = request.get_json()
    loc_id = payload["loc_id"]
    model_id = payload["model_id"]
    if not validate_integer_text_format(loc_id):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'Please check the entered strings they may not of the correct format'})
    device_id = str(getNextDeviceId())
    params = {'loc_id': loc_id, 'model_id': model_id, 'device_id': device_id}
    db.session.execute(text('''Insert into device (dev_id, loc_id, model_id) values
                       (:device_id, :loc_id, :model_id)'''), params)
    db.session.commit()
    return jsonify({'status': 'success', 'msg': 'Successfully added'})

# delete device
@devices.route("/devices/<dev_id>", methods=['DELETE'])
def deleteDevice(dev_id):
    if not validate_integer_text_format(dev_id):
        return render_template("error.html", error = {'status': 'validation error', 'message': 'Dev id not in correct format'})
    try:
        db.session.execute(text("Delete from device where dev_id=:id"), params={'id': dev_id})
        db.session.commit()
        return jsonify({'status': 'ok', 'msg': 'Record deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@devices.route("/devices/<dev_id>", methods=['PUT'])
def disableLocation(dev_id):
    try:
        db.session.execute(text('''update device set enabled=0 where dev_id=:dev_id'''), params={'dev_id': dev_id})
        db.session.commit()
        return jsonify({"status": 'success', 'message': 'Successfully disabled'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
def getNextDeviceId():
    # write a sequence in the database and get id from it
    last_db_id = db.session.execute(text("Select dev_id from device where dev_id REGEXP '^[0-9]+$' order by dev_id desc")).fetchone()
    last_db_id = last_db_id[0] if last_db_id else render_template("error.html", error = {'status': 'unexpected error', 'message': 'Unexpected error'})
    # try:
    #     last_db_id = int(last_db_id)
    # except Exception as e:
    #     last_db_id = '12334'
    return str(int(last_db_id)+1)