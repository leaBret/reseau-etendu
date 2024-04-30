import yaml

def update_hosts_yaml(file_path="fastprod/inventory/hosts.yaml", items=None):
    if items:
        with open(file_path,'w') as yaml_file:
            yaml.safe_dump(items, yaml_file)
    return True

def add_item_to_hosts_yaml(file_path="fastprod/inventory/hosts.yaml", save=True, item=None):
    with open(file_path,'r') as yaml_file:
        hosts = yaml.safe_load(yaml_file)
        new_hosts= hosts.copy()
        new_hosts[item.get('data').get('device_name')] = item
        if save:
            update_hosts_yaml(items=new_hosts)
    return new_hosts[item.get('data').get('device_name')]



def delete_item_from_hosts_yaml(yaml_file_path="fastprod/inventory/hosts.yaml", save=True, item=None, ):
    with open(yaml_file_path,'r') as yaml_file:
        hosts = yaml.safe_load(yaml_file)
        new_hosts = hosts.copy()
        del new_hosts[item.get('data').get('device_name')]
        if save:
            update_hosts_yaml(items=new_hosts)
    return True
