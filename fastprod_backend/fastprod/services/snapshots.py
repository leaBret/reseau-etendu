import os
from datetime import datetime
from services.config import get_config_by_device

def get_snapshot_by_name(name):
    from api import app
    files = os.listdir('fastprod/snapshots')
    snapshots = []
    for file in files:
        file_device_name = file.split('_')[0]
        if name == file:
            snapshots.append(dict(file=file, path='fastprod/snapshots', at=file.split('_')[1].split('.')[0]))
    return snapshots

def create_snapshot_by_device(device=None):
    from api import app
    nr = app.config.get('nr')
    config = get_config_by_device(device)
    file_path = 'fastprod/snapshots/{0}_{1}.conf'.format(device.get('name'), datetime.now())
    with open(file_path, 'w') as file:
        file.write(config.get('running'))
    return file_path

def get_snapshots_by_device(device):
    from api import app
    files = os.listdir('fastprod/snapshots')
    snapshots = []
    for file in files:
        file_device_name = file.split('_')[0]
        if file_device_name == device.get('name'):
            snapshots.append(dict(file=file, path='fastprod/snapshots', at=file.split('_')[1].split('.')[0]))
    return snapshots 

