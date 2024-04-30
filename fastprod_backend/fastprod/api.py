from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import json
from flask import jsonify, request, abort, make_response, jsonify, send_file
from nornir import InitNornir
from services.devices import ( get_inventory, add_device, get_device_by_name, delete_device, get_device_interfaces, get_device_interfaces_ip, get_device_facts)
from services.config import ( get_config_by_device )
from services.tasks import (run_show_commands_by_device, run_config_commands_by_device, run_config_from_file_by_device)
from werkzeug.utils import secure_filename
import os
from services.snapshots import ( get_snapshot_by_name, create_snapshot_by_device , get_snapshots_by_device)

ALLOWED_EXTENSIONS = {'conf'}
UPLOAD_FOLDER = 'fastprod/upload_files/'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route("/")
def welcome():
    return jsonify(
        env="DEV",
        name="fastprod_backend",
        version=1.0
    )

def init_nornir():
    app.config['nr'] = InitNornir(config_file="fastprod/inventory/config.yaml")

init_nornir()

@app.route("/devices", methods=['GET', 'POST'])
def devices():
    if request.method == 'GET':
        devices = get_inventory()
        return jsonify(devices=devices, total_count=len(devices))
    if request.method == 'POST':
        data = request.get_json()
        new_device = add_device(data)
        init_nornir() # apres avoir rajouter un host, on doit reinitialiser l'inventory 
        return jsonify(device=new_device)

@app.route("/devices/<device_name>", methods=['GET', 'DELETE'])
def device_by_name(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        return jsonify(device=device)
    if request.method == 'DELETE':
        device = get_device_by_name(device_name)
        delete_device(device)
        init_nornir()
        return jsonify(message="Device deleted")

@app.route("/devices/<device_name>/interfaces", methods=['GET'])
def get_interfaces(device_name):
    device = get_device_by_name(device_name)
    interfaces = get_device_interfaces( )
    return jsonify(interfaces=interfaces)

@app.route("/devices/<device_name>/interfaces/ip", methods=['GET'])
def get_interfaces_ip(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        interfaces_ip = get_device_interfaces_ip(device)
        return jsonify(interfaces_ip=interfaces_ip)

@app.route("/devices/<device_name>/facts", methods=['GET'])
def get_facts(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        facts = get_device_facts(device)
        return jsonify(facts=facts)

@app.route("/devices/<device_name>/config", methods=['GET','POST'])
def run_show_commands(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        config = get_config_by_device(device)
        return jsonify(facts=config)

    if request.method == 'POST':
        device = get_device_by_name(device_name)

        if request.files.to_dict(flat=False).get('config_file'):
            file = request.files.get('config_file')
            if allowed_file(file.filename) is False:
                abort(make_response(jsonify(message="file extension not allowed"), 403))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = run_config_from_file_by_device(device,file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(result=result)
        
        if request.get_json().get('mode') == 'enable':
            commands = request.get_json().get('commands')
            result = run_show_commands_by_device(device, commands=commands)
            return jsonify(result=result)

        if request.get_json().get('mode') == 'config':
            commands = request.get_json().get('commands')
            result = run_config_commands_by_device(device, commands=commands)
            return jsonify(result=result, commands=commands)

@app.route("/devices/<device_name>/snapshots", methods=['GET','POST'])
def get_snapshot_by_device(device_name):
    if request.method == 'GET':
        device = get_device_by_name(device_name)
        snapshots = get_snapshots_by_device(device)
        return jsonify(result=snapshots)
    if request.method == 'POST':
        device = get_device_by_name(device_name)
        snapshot = create_snapshot_by_device(device)
        result = get_snapshot_by_name(snapshot.split('/')[2])
        if result:
            result = True
        else :
            result = False
        return jsonify(result=result,snapshot=snapshot)

@app.route("/snapshots/<path:filename>", methods=['GET'])
def snapshot_by_name(filename):
    if request.method == 'GET':
        try:
            return send_file('snapshots/'+filename)
        except FileNotFoundError:
            abort(make_response(jsonify(message="snapshot not found"), 404))


