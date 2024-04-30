from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config, netmiko_commit

def run_show_commands_by_device(device=None, commands=[]):
    from api import app
    nr = app.config.get('nr')
    commands_sent = []
    if device:
        if len(commands) > 1:
            for command in commands:
                result = nr.filter(device_name=device.get('name')).run(task=napalm_cli,commands=[command])
                print_result(result)
                output = result[device.get('name')][0].result.get(command)
                commands_sent.append(dict(command=command, result=output))
            output = commands_sent
        else:
            result = nr.filter(device_name=device.get('name')).run(task=napalm_cli,commands=commands)
            output = result[device.get('name')][0].result.get(commands[0])
            commands_sent.append(dict(command=commands[0], result=output))
            output = commands_sent
    return output

def run_config_commands_by_device(device=None, commands=[]):
    from api import app
    nr = app.config.get('nr')
    commands_sent = []
    if device:
        result = nr.filter(device_name=device.get('name')).run(task=netmiko_send_config,config_commands=commands)
        print_result(result)
        return result[device.get('name')].changed

def run_config_from_file_by_device(device=None, file_path=None):
    from api import app
    nr = app.config.get('nr')
    if device and file_path:
        result = nr.filter(device_name=device.get('name')).run(task=netmiko_send_config,config_file=file_path)
        print_result(result)
        return result[device.get('name')].changed
