import json
from jinja2 import Template, Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader("templates"))


def load_json_data_from_file(file_path):
    try:
        with open(file_path) as json_file:
            data=json.load(json_file)
            print(data)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found",e)
    pass


def load_yaml_data_from_file(file_path):
    try:
        with open(file_path) as yaml_file:
            data = yaml.safe_load(yaml_file)
            print(data)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found", e)


def render_network_config(template_name, data):

    template = env.get_template(template_name)
    print(template.render(data))
    return template.render(data) 
    pass


def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass


if __name__ == "__main__":

    #process R2
    r2_data = load_yaml_data_from_file(file_path='data/R2.yaml')
    r2_config = render_network_config(template_name='R2.j2', data=r2_data)
    save_built_config('config/R2.conf', r2_config)

    #process ESW2
    esw4_data = load_yaml_data_from_file(file_path='data/ESW4.yaml')
    esw4_config = render_network_config(template_name='ESW4.j2', data=esw4_data)
    save_built_config('config/ESW4.conf', esw4_config)
    