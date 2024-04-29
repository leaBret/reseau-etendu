from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config, netmiko_commit


def question_13(nr):
    print(nr.__dict__)
    print(type(nr.__dict__))
    pass

def question_14(nr):
    print(nr.inventory.hosts)
    print(type(nr.inventory.hosts))
    pass

def question_15(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A'))
    print(type(nr.inventory.hosts.get('R1-CPE-BAT-A')))
    pass

def question_16(nr):
    print(dir(nr.inventory.hosts.get('R1-CPE-BAT-A')))
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').hostname)
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').username)
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').password)
    pass

def question_17(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').data['room'])
    pass

def question_18(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').data['room'])
    pass

def question_19(nr):
    print(nr.inventory.groups)
    pass

def question_20(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups)
    pass

def question_21(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].keys())
    pass

def question_22(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].values())
    pass

def question_23(nr):
    for i in nr.inventory.hosts :
        print(nr.inventory.hosts.get(str(i)).hostname)
    pass

def question_24(nr):
    print(nr.filter(device_type="router").inventory.hosts.keys())
    pass

def question_25(nr):
    print(nr.filter(device_type="router_switch").inventory.hosts.keys())
    pass


def hello_world(task: Task) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
    )

def question_26(nr):
    result = nr.run(task=hello_world)
    print(result)
    pass

def question_27(nr):
    result = nr.run(task=hello_world)
    print(type(result))
    pass

def question_28(nr):
    result = nr.run(task=hello_world)
    print(print_result(result))
    pass

def question_29(nr):
    result = nr.run(task=hello_world)
    print(print_result(result))
    pass

def question_30(nr):
    router_switch = nr.filter(device_type="router_switch")
    result = router_switch.run(task=hello_world)
    print(print_result(result))
    pass

def question_32(nr):
    router = nr.filter(device_type="router")
    result = nr.run(task=napalm_cli, commands=["sh ip int br"])
    print_result(result)
    pass
 
def question_33(nr):
    router_switch = nr.filter(device_type="router_switch")
    result = nr.run(task=napalm_get, getters=["arp_table"])
    print_result(result)
    pass

def question_34(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=napalm_configure, configuration="int lo1\nip address 1.1.1.1 255.255.255.255")
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=napalm_configure, configuration="int lo1\nip address 2.2.2.2 255.255.255.255")
    print_result(result)

    pass


def question_35(nr):
    result = nr.run(task=napalm_cli, commands=["wr"] ) 
    print_result(result)
    pass


def question_36(nr):
    router = nr.filter(device_type="router")
    result = nr.run(task=netmiko_send_command, command_string="sh ip int brief")
    print_result(result)

    pass

def question_37(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=netmiko_send_config, config_commands=["int lo2","ip address 1.1.1.2 255.255.255.255"])
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=netmiko_send_config, config_commands=["int lo2","ip address 2.2.2.3 255.255.255.255"])
    print_result(result)
    pass

def question_38(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=netmiko_save_config)
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=netmiko_save_config)
    print_result(result)
    pass

def question_39(nr):
    for host in nr.inventory.hosts:
        filename = list(host.split("-"))
        filename.insert(2, "LYON")
        filename = "_".join(filename)
        filename = f"config/{filename}.conf"
    
        with open(filename, 'r') as f:
            config_commands = f.readlines()
        result = nr.filter(device_name=host).run(task=netmiko_send_config, config_commands=config_commands) 
        print_result(result)
        result = nr.filter(device_name=host).run(task=netmiko_save_config) 
        print_result(result)
    pass

def question_39_d(nr):
        
    print('Avant shut interfaces')
    router_hosts = nr.filter(device_type="router")
    result = router_hosts.run(task=netmiko_send_command, command_string="show vrrp brief")
    print_result(result)

    print("On shut les interface des master\n")
    commands_BAT_B = [
        "interface GigabitEthernet3/0",  
        "shutdown",
    ]
    commands_BAT_A = [
        "interface GigabitEthernet2/0",  
        "shutdown",
    ]
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=netmiko_send_config, config_commands=commands_BAT_A)
    result = nr.filter(device_name="R2-CPE-BAT-B").run(task=netmiko_send_config, config_commands=commands_BAT_B)

    print('Après shut interfaces')
    result = router_hosts.run(task=netmiko_send_command, command_string="show vrrp brief")
    print_result(result)

    pass

def render_network_config(template_name, data):
    try:
        template = env.get_template(template_name) 
        print(template.render(data))
        return template.render(data)
    except:
        print("Une erreur est parvenue")
    pass



def save_built_config(file_name, data):

    import os
    directory = os.path.dirname(file_name)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, 'w') as file:
        file.write(data)
    pass

def load_yaml_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            print(data)
        return data
    except FileNotFoundError as e:
        print('Erreur retournée: File not found')
    pass

def create_config_ospf():
    hosts = load_yaml_data_from_file(file_path = 'data/ospf_R1_CPE_BAT_A.yaml')
    ospf_R1_CPE_BAT_A = render_network_config(template_name='ospf.j2', data=  hosts)
    save_built_config('config/ospf_R1_CPE_BAT_A.conf', ospf_R1_CPE_BAT_A)

    hosts1 = load_yaml_data_from_file(file_path = 'data/ospf_R2_CPE_BAT_A.yaml')
    ospf_R2_CPE_BAT_A = render_network_config(template_name='ospf.j2', data=  hosts1)
    save_built_config('config/ospf_R2_CPE_BAT_A.conf', ospf_R2_CPE_BAT_A)

    hosts2 = load_yaml_data_from_file(file_path = 'data/ospf_R1_CPE_BAT_B.yaml')
    ospf_R1_CPE_BAT_B = render_network_config(template_name='ospf.j2', data=  hosts2)
    save_built_config('config/ospf_R1_CPE_BAT_B.conf', ospf_R1_CPE_BAT_B)

    hosts3 = load_yaml_data_from_file(file_path = 'data/ospf_R2_CPE_BAT_B.yaml')
    ospf_R2_CPE_BAT_B = render_network_config(template_name='ospf.j2', data=  hosts3)
    save_built_config('config/ospf_R2_CPE_BAT_B.conf', ospf_R2_CPE_BAT_B)
    pass

def question_40(nr):
    create_config_ospf()
    for host in nr.inventory.hosts:
        filename = list(host.split("-"))
        filename.insert(0, "ospf")
        filename = "_".join(filename)
        filename = f"config/{filename}.conf"
        #print(filename)
        #print(host)
        if not os.path.isfile(filename):
            print("Aucun fichier trouvé")
            continue
    
        with open(filename, 'r') as f:
            config_commands = f.readlines()
        result = nr.filter(device_name=host).run(task=netmiko_send_config, config_commands=config_commands) 
        print_result(result)
        result = nr.filter(device_name=host).run(task=netmiko_save_config) 
        print_result(result)
    

    pass

    

if __name__ == "__main__":
    nr = InitNornir(config_file="inventory/config.yaml")

    # question_13(nr)
    # question_14(nr)
    # question_15(nr)
    # question_16(nr)
    # question_17(nr)
    #question_18(nr)
    # question_19(nr)
    # question_20(nr)
    # question_21(nr)
    # question_22(nr)
    # question_23(nr)
    # question_24(nr)
    # question_25(nr)
    # question_26(nr)
    # question_27(nr)
    # question_28(nr)
    # question_29(nr)
    # question_30(nr)

    #question_32(nr)
    # question_33(nr)
    #question_34(nr)
    #question_35(nr)
    #question_36(nr)
    #question_37(nr)
    #question_38(nr)
    # question_39(nr)
    # question_39_d(nr)

    question_40(nr)
    pass
