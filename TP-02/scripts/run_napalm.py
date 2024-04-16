import json
from napalm import get_network_driver

def get_inventory():
    pass


def get_json_data_from_file(file):
    pass

def question_26(device):
    device.open()
    output = device.cli(['show ip interface brief'])
    print(output)
    device.close()
    pass


def question_27(device):
    print(type(output))
    pass

def question_28(device):
    device.open()
    output = device.get_arp_table()
    print(output)
    device.close()
    pass

def question_29(device):
    print(type(output))
    pass


def question_30(device):
    device.open()
    with open('config/loopback R01.conf', 'r') as config_file:
        config = config_file.read()

    device.load_merge_candidate(config=config)
    print("Changements :")
    print(device.compare_config())

    device.commit_config()
    device.close()
    pass



def question_31():
    router_names = ['r01', 'r02', 'r03']
    for router_name in router_names:
        data = load_yaml_data_from_file(file_path=f'data/ospf_{router_name}.yaml')
        config = render_network_config(template_name='ospf.j2', data=data)
        save_built_config(f'config/ospf_{router_name}.config', config)
    pass


def question_32():

    hosts = get_inventory()

    for i in hosts :
        if i['hostname'].startswith(("R01","R02","R03")):
            
            ri = {
                    'hostname': i['ip'],
                    'username': i['username'],
                    'password': i['password']
            }

            driver = get_network_driver('ios')
            device  = driver(**ri)

            device.open()

            # Charger le contenu du fichier de configuration dans une variable
            with open(f'config/ospf_{i["hostname"].lower()}.config', 'r') as config_file:
                config = config_file.read()

            device.load_merge_candidate(config=config)

            # Afficher les changements proposés
            print("Changements proposés:")
            print(device.compare_config())

            device.commit_config()

            # Fermer la session avec le périphérique
            device.close()
    pass


def question_34():

    hosts = get_inventory()
    for i in hosts :
            
        ri = {
                'hostname': i['ip'],
                'username': i['username'],
                'password': i['password']
        }

        driver = get_network_driver('ios')
        device  = driver(**ri)
        device.open()
        data = device.get_config('running')

        with open(f'config/backup/{i["hostname"]}.backup', 'w') as f:
            f.write(data['running'])

        print('enregistrement effectué')

        device.close()
    pass



if __name__ == "__main__":
    r01 = {
    'hostname':'172.16.100.126',
    'username': cisco,
    'password': cisco
    }

    driver = get_network_driver('ios')
    device  = driver(**r01)
    device.open()
    
    question_26(device)
    question_27(device)
    question_28(device)
    question_29(device)
    question_30(device)
    question_31()
    question_32()
    question_34()