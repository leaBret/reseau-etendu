import json
from netmiko import ConnectHandler
import re

def question_9(net_connect):
    print("host est ", net_connect.host, "et le Device type est ", net_connect.device_type)

def question_10(net_connect):
    command = "show ip interface brief"
    with net_connect:
        output = net_connect.send_command(command)

    print(f"{output}")
    pass

def question_11(net_connect):
    command = "show ip interface brief"
    with net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print(f"{output}")
    pass


def question_12(net_connect):
    command = "show ip route"

    with net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print(f"{output}")
    pass

def question_13(net_connect):
    command = "show ip interface brief"

    with net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
        print(f"{output}")

        for i in output: 
            command2 = f'show ip interface {i["interface"]}'
            print(command2)
            output2 = net_connect.send_command_expect(command2, use_textfsm=True)
            print(f"{output2}")

    net_connect.disconnect()
    pass


def question_14(net_connect):
    command = [
        'interface loopback 1',
        'ip address 192.168.1.1 255.255.255.255',
        'description loopback interface from netmiko',
        'no shutdown'
    ]

    with net_connect:
        output = net_connect.send_config_set(command)
        output += net_connect.save_config()
        
        print(f"{output}")
    pass


def question_15(net_connect):
    command = [
        'no interface loopback 1'
    ]

    with net_connect:
        output = net_connect.send_config_set(command)
        output += net_connect.save_config()

        print(f"{output}")
    pass

def question_16(net_connect):
    cfg_file = "config/loopback_R01.conf"
    with net_connect:
        output = net_connect.send_config_from_file(cfg_file)
        output += net_connect.save_config()
    print(f"{output}")
    pass


def question_17(net_connect):
    commands = [
        'no interface loopback 1',
        'no interface loopback 2',
        'no interface loopback 3',
        'no interface loopback 4'
    ]

    with net_connect:
        output = net_connect.send_config_set(commands)
        output += net_connect.save_config()
        print(f"{output}")
    pass

def get_inventory():
    file_path = "inventory/hosts.json"
    with open(file_path, "r") as file:
        inventory_data = json.load(file)
    return inventory_data


def question_20(hosts):
    for host in hosts :
        if re.match(r'^R', host['hostname']):
            print(host['hostname'])

            device = {
                'device_type': 'cisco_ios',
                'host': host['ip'],
                'username': host['username'],
                'password': host['password'],
            }

            with ConnectHandler(**device) as net_connect :
                command = 'show ip int g0/0.99'
                output= net_connect.send_command(command, use_textfsm=True)
                print(f"{output}")
                net_connect.disconnect()
    pass



def question_21(hosts):
    for host in hosts :
        if re.match(r'^MARSEILLE', host['site']) or re.match(r'^PARIS', host['site']):

            print(host['hostname'])

            device = {
                'device_type': 'cisco_ios',
                'host': host['ip'],
                'username': host['username'],
                'password': host['password'],
            }

            cfg_file = f'config/vlan_{host["hostname"]}.conf'
            with ConnectHandler(**device) as net_connect :
                output = net_connect.send_config_from_file(cfg_file)
                output += net_connect.save_config()

                print(f"{output}")

                net_connect.disconnect()
    pass


if __name__ == "__main__":    
    r01 = {
        'device_type': 'cisco_ios',
        'host':   '172.16.100.62',
        'username': 'cisco',
        'password': 'cisco'
    }
    net_connect = ConnectHandler(**r01)
    
    # question_9(net_connect)
    # question_10(net_connect)
    # question_11(net_connect)
    #question_12(net_connect)
    #question_13(net_connect)
    #question_14(net_connect)
    #question_15(net_connect)
    #question_16(net_connect)
    #question_17(net_connect)
    hosts = get_inventory()
    # print(hosts)
    # question_20(hosts)
    question_21(hosts)