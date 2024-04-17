import json
from jinja2 import Template, Environment,  FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


def load_json_data_from_file(file_path):
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            print(data)
        return data
    except FileNotFoundError as e: 
        print("Erreur, chemin de fichier introuvable", e)
    pass

def render_network_config(template_name, data):
    template = env.get_template(template_name)
    print(template.render(data))
    return template.render(data) 
    pass

def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass


def create_config_cpe_lyon_batA():

    config={}

    data = load_json_data_from_file(file_path=f'data/R1_CPE_LYON_BAT_A.json')
    config_r1_cpe_bat_lyon_a = render_network_config(template_name='vlan_router.j2', data=data)
    config['r1']= config_r1_cpe_bat_lyon_a

    data = load_json_data_from_file(file_path=f'data/R2_CPE_LYON_BAT_A.json')
    config_r2_cpe_bat_lyon_a = render_network_config(template_name='vlan_router.j2', data=data)
    config['r2']= config_r2_cpe_bat_lyon_a

    data = load_json_data_from_file(file_path=f'data/ESW1_CPE_LYON_BAT_A.json')
    config_esw1_cpe_bat_lyon_a = render_network_config(template_name='vlan_switch.j2', data=data)
    config['esw1']= config_esw1_cpe_bat_lyon_a

    return config
   


def create_config_cpe_lyon_batB():
    config={}

    data = load_json_data_from_file(file_path=f'data/R1_CPE_LYON_BAT_B.json')
    config_r1_cpe_bat_lyon_b = render_network_config(template_name='vlan_router.j2', data=data)
    config['r1']= config_r1_cpe_bat_lyon_b

    data = load_json_data_from_file(file_path=f'data/R2_CPE_LYON_BAT_B.json')
    config_r2_cpe_bat_lyon_b = render_network_config(template_name='vlan_router.j2', data=data)
    config['r2']= config_r2_cpe_bat_lyon_b

    data = load_json_data_from_file(file_path=f'data/ESW1_CPE_LYON_BAT_B.json')
    config_esw1_cpe_bat_lyon_b = render_network_config(template_name='vlan_switch.j2', data=data)
    config['esw1']= config_esw1_cpe_bat_lyon_b

    return config
    
if __name__ == "__main__":
    """
        process question 3 to 5:
    """
    # question 3:
    config = create_config_cpe_lyon_batA()

    #question 4:
    save_built_config('config/R1_CPE_LYON_BAT_A.conf', config.get('r1'))
    save_built_config('config/R2_CPE_LYON_BAT_A.conf', config.get('r2'))
    save_built_config('config/ESW1_CPE_LYON_BAT_A.conf', config.get('esw1'))

    #question 5:
    config = create_config_cpe_lyon_batB()
    save_built_config('config/R1_CPE_LYON_BAT_B.conf', config.get('r1'))
    save_built_config('config/R2_CPE_LYON_BAT_B.conf', config.get('r2'))
    save_built_config('config/ESW1_CPE_LYON_BAT_B.conf', config.get('esw1'))
    