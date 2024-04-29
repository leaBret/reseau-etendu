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
   
    config = {}

    print("######### R1_CPE_LYON_BAT_A")
    r1_data_batA = load_json_data_from_file(file_path='data/R1_CPE_LYON_BAT_A.json')
    r1_config_batA = render_network_config(template_name='vlan_router.j2', data=r1_data_batA)
    r1_vrrp_config_batA  = render_network_config(template_name='vrrp_router.j2', data=r1_data_batA)

    r1 = r1_config_batA + "\n\n" + r1_vrrp_config_batA
    config['r1'] = r1

    print("######### ESW1_CPE_LYON_BAT_A")
    esw1_data_batA = load_json_data_from_file(file_path='data/ESW1_CPE_LYON_BAT_A.json')
    esw1 = render_network_config(template_name='vlan_switch.j2', data=esw1_data_batA)
    config['esw1'] = esw1

    print("######### R2_CPE_LYON_BAT_A")
    r2_data_batA = load_json_data_from_file(file_path='data/R2_CPE_LYON_BAT_A.json')
    r2_config_batA = render_network_config(template_name='vlan_router.j2', data=r2_data_batA)
    r2_vrrp_config_batA = render_network_config(template_name='vrrp_router.j2', data=r2_data_batA)

    r2 = r2_config_batA + "\n\n" + r2_vrrp_config_batA
    config['r2'] = r2
    return config
    pass
    

def create_config_cpe_lyon_batB():
    config = {}

    print("######### R1_CPE_LYON_BAT_B")
    r1_data_batB = load_json_data_from_file(file_path='data/R1_CPE_LYON_BAT_B.json')
    r1_config_batB = render_network_config(template_name='vlan_router.j2', data=r1_data_batB)
    r1_config_batB = render_network_config(template_name='vlan_router.j2', data=r1_data_batB)
    r1_vrrp_config_batB  = render_network_config(template_name='vrrp_router.j2', data=r1_data_batB)

    r1 = r1_config_batB + "\n\n" + r1_vrrp_config_batB
    config['r1'] = r1

    print("######### ESW1_CPE_LYON_BAT_B")
    esw1_data_batB = load_json_data_from_file(file_path='data/ESW1_CPE_LYON_BAT_B.json')
    esw1 = render_network_config(template_name='vlan_switch.j2', data=esw1_data_batB)
    config['esw1'] = esw1

    print("######### R2_CPE_LYON_BAT_B")
    r2_data_batB = load_json_data_from_file(file_path='data/R2_CPE_LYON_BAT_B.json')
    r2_config_batB = render_network_config(template_name='vlan_router.j2', data=r2_data_batB)
    r2_vrrp_config_batB = render_network_config(template_name='vrrp_router.j2', data=r2_data_batB)

    r2 = r2_config_batB + "\n\n" + r2_vrrp_config_batB
    config['r2'] = r2
    return config
    pass
    
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
    