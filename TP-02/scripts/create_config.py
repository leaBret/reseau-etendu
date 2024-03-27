import json
from jinja2 import Template, Environment,  FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def load_json_data_from_file(file_path):
    try:
        with open(file_path) as json_file:
            data=json.load(json_file)
            print(data)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found",e)


def render_network_config(template_name, data):
    template = env.get_template(template_name)
    print(template.render(data))
    return template.render(data) 


def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass


def create_vlan_config_cpe_marseille():
    r2_data = load_json_data_from_file(file_path='data/vlan_R02.json')
    r2_config = render_network_config(template_name='vlan_router.j2', data=r2_data)
    esw2_data = load_json_data_from_file(file_path='data/vlan_ESW2.json')
    esw2_config = render_network_config(template_name='vlan_switch.j2', data=esw2_data)
    return r2_config, esw2_config


def create_vlan_config_cpe_paris():
    r3_data = load_json_data_from_file(file_path='data/vlan_R03.json')
    r3_config = render_network_config(template_name='vlan_router.j2', data=r3_data)
    esw3_data = load_json_data_from_file(file_path='data/vlan_ESW3.json')
    esw3_config = render_network_config(template_name='vlan_switch.j2', data=esw3_data)
    return r3_config, esw3_config


if __name__ == "__main__":
    """
        process question 1 to 5:
    """
    r02_config, esw2_config = create_vlan_config_cpe_marseille()
    save_built_config('config/vlan_R02.conf', r02_config)
    save_built_config('config/vlan_ESW2.conf', esw2_config)
    
    r03_config, esw3_config = create_vlan_config_cpe_paris()
    save_built_config('config/vlan_R03.conf', r03_config)
    save_built_config('config/vlan_ESW3.conf', esw3_config)

