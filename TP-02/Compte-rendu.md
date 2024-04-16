# Compte rendu TP2 Automatisation réseau

## Génération automatique de la configuration à l’aide de Jinja2 (TP-01)

Rappel, pour lancer le script : 

```sh
pipenv install jinja2
pipenv shell
python3 -m scripts.create_config
```

### 1) Développez l’ensemble des templates Jinja2 qui vous permettront de générer la configuration nécessaire pour le bon fonctionnement du site CPE-MARSEILLE. 


Pour le fichier vlan_router.j2 : 

```j2
{% for interface in interfaces %}
interface {{ interface.name }}
description {{ interface.description }}
{% if 'vlan_id' in interface %}
encapsulation dot1Q {{ interface.vlan_id }}
{% endif %}
ip address {{ interface.ip }} {{ interface.netmask }}
{% if '.' in interface.name %}
interface {{ interface.name.split('.')[0] }}
no shutdown
{% endif %}
exit
{% endfor %}
end
write

```

Pour le fichier vlan_switch.j2 : 

```j2
{% for vlan in vlans %}
vlan {{ vlan.id }}
name {{ vlan.name }}
{% endfor %}

{% for interface in interfaces %}

{% if interface.vlan_mode == "trunk" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport trunk allowed vlan add {{ interface.vlan_allowed|join(', ')  }}
{% endif %}

{% if interface.vlan_mode == "access" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport access vlan {{ interface.vlan_id }}
{% endif %}

{% if interface.ip %}
interface {{ interface.name }}
ip address {{ interface.ip }} {{ interface.masque }}
no shutdown
{% endif %}


no shutdown
exit
{% endfor %}
end
write

```

### 2) Définissez les structures de données dans des fichiers JSON ou YAML nécessaires pour remplir votre template JInja2 développé à la question

(Pour rappel, le vlan d’admin (99) est déjà configuré sur les équipements.)


Pour vlan_ESW2.json :

```json

{
	"vlans":[
    	{
    	"name":"teacher",
    	"id":"10"
    	},
    	{
    	"name":"student",
    	"id":"20"
    	}
	],
	"interfaces": [
    	{
    	"name": "f1/1",
    	"vlan_mode":"access",
    	"description": "Switch interface for teacher LAN",
    	"vlan_id": "10"
    	},
    	{
    	"name": "f1/2",
    	"vlan_mode":"access",
    	"description": "Switch interface for student LAN",
    	"vlan_id": "20"
    	},
    	{
    	"name": "f1/0",
    	"vlan_mode":"trunk",
    	"description": "Switch interface for Trunk",
    	"vlan_allowed": ["10","20","99"]
    	}
	]
}
```



Pour vlan_R02.json :

```json
{
    "interfaces":
    [
        {
            "name": "g0/0",
            "description":"Gateway interface"
        },
        {
        "name": "g0/0.10",
        "description": "Gateway interface for teacher LAN",
        "ip": "172.16.30.254",
        "mask": "255.255.255.0",
        "vlan_id": "10"
        },
        {
        "name": "g0/0.20",
        "description": "Gateway interface for student LAN",
        "ip": "172.16.40.254",
        "mask": "255.255.255.0",
        "vlan_id": "20"
        }
    ]
}

```

### 3) Développez les fonctions vous permettant de générer automatiquement les configurations à partir du template Jinja2 et de la structure de données. 

Dans create_config.py : 

```python

def load_json_data_from_file(file_path):
    try:
        with open(file_path) as json_file:
            data=json.load(json_file)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found",e)

def render_network_config(template_name, data):
    template = env.get_template(template_name)
    return template.render(data) 

def create_vlan_config_cpe_marseille():
    r2_data = load_json_data_from_file(file_path='data/vlan_R02.json')
    r2_config = render_network_config(template_name='vlan_router.j2', data=r2_data)
    esw2_data = load_json_data_from_file(file_path='data/vlan_ESW2.json')
    esw2_config = render_network_config(template_name='vlan_switch.j2', data=esw2_data)
    return r2_config, esw2_config

```

### 4) Développez les fonctions vous permettant de sauvegarder automatiquement les configurations générées dans le dossier config de votre workspace

Dans le fichier create-config.py : 

```python
def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass

if __name__ == "__main__":
    """
        process question 1 to 5:
    """
    r02_config, esw2_config = create_vlan_config_cpe_marseille()
    save_built_config('config/vlan_R02.conf', r02_config)
    save_built_config('config/vlan_ESW2.conf', esw2_config)
    pass

```

### 5) Répétez les questions 1 à 4 pour le site CPE-PARIS

Faites vérifier le résultat par votre responsable pédagogique
A ce stade le main de votre script python ne doit contenir que l’appel aux
fonctions :
● create_vlan_config_cpe_marseille()
● create_vlan_config_cpe_paris()
● save_built_config()
Aucune configuration ne doit être implémentée sur les équipements pour le
moment. Nous reviendrons sur ces éléments de configurations un peu plus
tard dans le TP.


Pour la fichier vlan_ESW3.json :

```json
{
	"vlans":[
    	{
    	"name":"teacher",
    	"id":"10"
    	},
    	{
    	"name":"student",
    	"id":"20"
    	}
	],
	"interfaces": [
    	{
    	"name": "f1/1",
    	"vlan_mode":"access",
    	"description": "Switch interface for teacher LAN",
    	"vlan_id": "10"
    	},
    	{
    	"name": "f1/2",
    	"vlan_mode":"access",
    	"description": "Switch interface for student LAN",
    	"vlan_id": "20"
    	},
    	{
    	"name": "f1/0",
    	"vlan_mode":"trunk",
    	"description": "Switch interface for Trunk",
    	"vlan_allowed": ["10","20","99"]
    	}
	]
}

```

Pour le fichier vlan_R03.json : 

```json
{
    "interfaces":
    [
        {
            "name": "g0/0",
            "description":"Gateway interface"
        },
        {
        "name": "g0/0.10",
        "description": "Gateway interface for teacher LAN",
        "ip": "172.16.50.254",
        "mask": "255.255.255.0",
        "vlan_id": "10"
        },
        {
        "name": "g0/0.20",
        "description": "Gateway interface for student LAN",
        "ip": "172.16.60.254",
        "mask": "255.255.255.0",
        "vlan_id": "20"
        }
    ]
}

```


Dans le script create_config.py : 

```python
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

    pass
```

## 4. Automatisation réseau avec netmiko

```sh
pipenv install netmiko
```

Se connecter au routeur R1: 

```python
if __name__ == "__main__":    
    r01 = {
        'device_type': 'cisco_ios',
        'host':   '172.16.100.62',
        'username': 'cisco',
        'password': 'cisco'
    }
    net_connect = ConnectHandler(**r01)

```
### 9) Affichez la variable net_connect. Que contient la variable ? Quels sont les attributs de la variable ?

La variable net_connect est un objet. 

Ses sttributs sont :
```sh
{'remote_conn': <paramiko.Channel 0 (open) window=8153 -> <paramiko.Transport at 0x30c4edc0 (cipher aes128-cbc, 128 bits) (active; 1 open channel(s))>>, '_config_mode': True, '_read_buffer': '', 'delay_factor_compat': False, 'TELNET_RETURN': '\r\n', 'RETURN': '\n', 'RESPONSE_RETURN': '\n', 'disable_lf_normalization': False, 'host': '172.16.100.62', 'port': 22, 'username': 'cisco', 'password': 'cisco', 'secret': '', 'device_type': 'cisco_ios', 'ansi_escape_codes': False, 'verbose': False, 'auth_timeout': None, 'banner_timeout': 15, 'blocking_timeout': 20, 'conn_timeout': 10, 'session_timeout': 60, 'timeout': 100, 'read_timeout_override': None, 'keepalive': 0, 'allow_auto_change': False, 'encoding': 'utf-8', 'sock': None, 'sock_telnet': None, 'fast_cli': True, '_legacy_mode': False, 'global_delay_factor': 0.1, 'global_cmd_verify': None, 'session_log': None, '_session_log_close': False, 'serial_settings': {'port': 'COM1', 'baudrate': 9600, 'bytesize': 8, 'parity': 'N', 'stopbits': 1}, 'base_prompt': 'R1', '_session_locker': <unlocked _thread.lock object at 0x7fcc325f45a0>, 'protocol': 'ssh', 'key_policy': <paramiko.client.AutoAddPolicy object at 0x7fcc32419d60>, 'use_keys': False, 'key_file': None, 'pkey': None, 'passphrase': None, 'allow_agent': False, 'system_host_keys': False, 'alt_host_keys': False, 'alt_key_file': '', 'disabled_algorithms': {}, 'ssh_config_file': None, 'remote_conn_pre': <paramiko.client.SSHClient object at 0x7fcc32419d90>, 'channel': <netmiko.channel.SSHChannel object at 0x7fcc323b01f0>}
(TP-02-JgfHG1d0
```

Affichez, l’adresse ip et le device type de l’objet net_connect : 

```python

def question_9(net_connect):
    print("l'host est ", net_connect.host, "et le Device type est ", net_connect.device_type)

if __name__ == "__main__":    
    question_9(net_connect)
```

l'host est  172.16.100.62 et le Device type est  cisco_ios


### 10) Quelle méthode de l’objet net_connect permet d'exécuter des commandes “show” ? Affichez l’état des interfaces du routeur R1 depuis le script run_netmiko.

```python

def question_10(net_connect):
    command = "show ip interface brief"
    with net_connect:
        output = net_connect.send_command(command)

    print(f"{output}")
    pass
```

le résulat : 

```sh
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/0         unassigned      YES NVRAM  up                    up      
GigabitEthernet0/0.10      172.16.10.254   YES NVRAM  up                    up      
GigabitEthernet0/0.20      172.16.20.254   YES NVRAM  up                    up      
GigabitEthernet0/0.99      172.16.100.126  YES NVRAM  up                    up      
Serial1/0                  10.1.1.1        YES NVRAM  up                    up      
Serial1/1                  10.1.3.1        YES NVRAM  up                    up      
Serial1/2                  unassigned      YES NVRAM  administratively down down    
Serial1/3                  unassigned      YES NVRAM  administratively down down    
GigabitEthernet2/0         172.16.100.62   YES NVRAM  up                    up  
```


### 11) Utilisez le paramètre use_textfsm=True à la commande de la question précédente et affichez le résultat, qu’observez-vous ?


```python
def question_11(net_connect):
    command = "show ip interface brief"
    with net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print(f"{output}")
    pass

```

le résultat : 
```sh
[{'interface': 'Ethernet0/0', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'GigabitEthernet0/0', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.10', 'ip_address': '172.16.10.254', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.20', 'ip_address': '172.16.20.254', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.99', 'ip_address': '172.16.100.126', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/0', 'ip_address': '10.1.1.1', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/1', 'ip_address': '10.1.3.1', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/2', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'Serial1/3', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'GigabitEthernet2/0', 'ip_address': '172.16.100.62', 'status': 'up', 'proto': 'up'}]
```

On remarque que le format est maintenant une liste de dictionnaires 


### 12) Affichez la table de routage du routeur R1 en utilisant le paramètre textfsm. Quel est le format de données retourné ?

```python
def question_12(net_connect):
    command = "show ip route"

    with net_connect:
        output = net_connect.send_command(command, use_textfsm=True)
    print(f"{output}")
    pass
```
Le résulat est : 

```sh
[{'vrf': '', 'protocol': 'S', 'type': '', 'network': '172.16.100.192', 'prefix_length': '26', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'Serial1/1', 'uptime': ''}, {'vrf': '', 'protocol': 'S', 'type': '', 'network': '172.16.100.128', 'prefix_length': '26', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'Serial1/0', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '172.16.100.64', 'prefix_length': '26', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'GigabitEthernet0/0.99', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '172.16.20.0', 'prefix_length': '24', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'GigabitEthernet0/0.20', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '172.16.10.0', 'prefix_length': '24', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'GigabitEthernet0/0.10', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '172.16.100.0', 'prefix_length': '26', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'GigabitEthernet2/0', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '10.1.3.0', 'prefix_length': '30', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'Serial1/1', 'uptime': ''}, {'vrf': '', 'protocol': 'C', 'type': '', 'network': '10.1.1.0', 'prefix_length': '30', 'distance': '', 'metric': '', 'nexthop_ip': '', 'nexthop_vrf': '', 'nexthop_if': 'Serial1/0', 'uptime': ''}]
```

On remarque que le format est maintenant une liste de dictionnaires 

### 13) Affichez l’état des interfaces du routeur R1 et dans un second temps afficher la configuration de chacune des interfaces retournée par la première commande.

```python
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
```

Le résultat est : 

```sh
[{'interface': 'Ethernet0/0', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'GigabitEthernet0/0', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.10', 'ip_address': '172.16.10.254', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.20', 'ip_address': '172.16.20.254', 'status': 'up', 'proto': 'up'}, {'interface': 'GigabitEthernet0/0.99', 'ip_address': '172.16.100.126', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/0', 'ip_address': '10.1.1.1', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/1', 'ip_address': '10.1.3.1', 'status': 'up', 'proto': 'up'}, {'interface': 'Serial1/2', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'Serial1/3', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'}, {'interface': 'GigabitEthernet2/0', 'ip_address': '172.16.100.62', 'status': 'up', 'proto': 'up'}]
show ip interface Ethernet0/0
[{'interface': 'Ethernet0/0', 'link_status': 'administratively down', 'protocol_status': 'down', 'ip_address': [], 'prefix_length': [], 'vrf': '', 'mtu': '', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface GigabitEthernet0/0
[{'interface': 'GigabitEthernet0/0', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': [], 'prefix_length': [], 'vrf': '', 'mtu': '', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface GigabitEthernet0/0.10
[{'interface': 'GigabitEthernet0/0.10', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.10.254'], 'prefix_length': ['24'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface GigabitEthernet0/0.20
[{'interface': 'GigabitEthernet0/0.20', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.20.254'], 'prefix_length': ['24'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface GigabitEthernet0/0.99
[{'interface': 'GigabitEthernet0/0.99', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.100.126'], 'prefix_length': ['26'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface Serial1/0
[{'interface': 'Serial1/0', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['10.1.1.1'], 'prefix_length': ['30'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface Serial1/1
[{'interface': 'Serial1/1', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['10.1.3.1'], 'prefix_length': ['30'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface Serial1/2
[{'interface': 'Serial1/2', 'link_status': 'administratively down', 'protocol_status': 'down', 'ip_address': [], 'prefix_length': [], 'vrf': '', 'mtu': '', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface Serial1/3
[{'interface': 'Serial1/3', 'link_status': 'administratively down', 'protocol_status': 'down', 'ip_address': [], 'prefix_length': [], 'vrf': '', 'mtu': '', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
show ip interface GigabitEthernet2/0
[{'interface': 'GigabitEthernet2/0', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.100.62'], 'prefix_length': ['26'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
```

### 14) Quelle méthode de l’objet net_connect permet d'exécuter des commandes en mode config ? 

la méthode est send_config_set

#### Créez une interface loopback sur le routeur R1. Utilisez la méthode save_config de netmiko pour sauvegarder automatiquement la config.

nom de l’interface : loopback 1
ip de l’interface : 192.168.1.1/32
description: “loopback interface from netmiko”

```python

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

```

le résultat : 

```sh
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface loopback 1
R1(config-if)#ip address 192.168.1.1 255.255.255.255
R1(config-if)#description loopback interface from netmiko
R1(config-if)#no shutdown
R1(config-if)#end
R1#write mem
Building configuration...
[OK]
R1#
```

Et si on vérifie sur le router, l'interface de loopback 1 à bien été modifié 

### 15) Supprimez l’interface loopback 1 depuis le script netmiko

```python
def question_15(net_connect):
    command = [
        'no interface loopback 1'
    ]

    with net_connect:
        output = net_connect.send_config_set(command)
        output += net_connect.save_config()

        print(f"{output}")
    pass

```

Résulat : 

```sh
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#no interface loopback 1
R1(config)#end
R1#write mem
Building configuration...
[OK]
R1#
```

#### a) Déployez la configuration du fichier loopback_r01.conf depuis netmiko.

```python
def question_16(net_connect):
    cfg_file = "config/loopback_R01.conf"
    with net_connect:
        output = net_connect.send_config_from_file(cfg_file)
        output += net_connect.save_config()
    print(f"{output}")
    pass
```

Résulat : 

```sh
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface loopback 1
R1(config-if)#ip address 192.168.1.1 255.255.255.255
R1(config-if)#description "interface loopback 1"
R1(config-if)#no shut
R1(config-if)#
R1(config-if)#interface loopback 2
R1(config-if)#ip address 192.168.2.1 255.255.255.255
R1(config-if)#description "interface loopback 2"
R1(config-if)#no shut
R1(config-if)#
R1(config-if)#interface loopback 3
R1(config-if)#ip address 192.168.3.1 255.255.255.255
R1(config-if)#description "interface loopback 3"
R1(config-if)#no shut
R1(config-if)#
R1(config-if)#interface loopback 4
R1(config-if)#ip address 192.168.4.1 255.255.255.255
R1(config-if)#description "interface loopback 4"
R1(config-if)#no shut
R1(config-if)#end
R1#write mem
Building configuration...
[OK]
R1#
```

##### b) Quelle est l’autre option possible pour déployer ce fichier de configuration depuis netmiko?

Nous pouvons créer un dictionnaire ceci : 

```python
def question_16(net_connect):
    commands = [
        'interface loopback 1',
        'ip address 192.168.1.1 255.255.255.255',
        'description “interface loopback 1”',
        'no shutdown',
        'interface loopback 2',
        'ip address 192.168.2.1 255.255.255.255',
         'description “interface loopback 2”',
        'no shutdown',
        'interface loopback 3',
        'ip address 192.168.3.1 255.255.255.255',
        'description “interface loopback 3”',
        'no shutdown',
        'interface loopback 4',
        'ip address 192.168.4.1 255.255.255.255',
        'description “interface loopback 4”',
        'no shutdown'
    ]
    with net_connect:
        output = net_connect.send_config_from_file(commands)
        output += net_connect.save_config()
    print(f"{output}")
    pass
```

### 16) Supprimez les interfaces loopback du routeur r01 depuis netmiko.

```python
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
```

Les interfaces ont été supprimées.

### 17) Supprimez les interfaces loopback du routeur r01 depuis netmiko.

```python
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
```

### 19) Développez une fonction get_inventory qui retourne le contenu du fichier inventory/hosts.json

```python
def get_inventory():
    file_path = "inventory/hosts.json"
    with open(file_path, "r") as file:
        inventory_data = json.load(file)
    return inventory_data
```

Résultat :

```sh
[{'hostname': 'R01', 'ip': '172.16.100.126', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}, {'hostname': 'R02', 'ip': '172.16.100.190', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}, {'hostname': 'R03', 'ip': '172.16.100.254', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}, {'hostname': 'ESW1', 'ip': '172.16.100.125', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}, {'hostname': 'ESW2', 'ip': '172.16.100.189', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}, {'hostname': 'ESW3', 'ip': '172.16.100.253', 'device_type': 'cisco_ios', 'username': 'cisco', 'password': 'cisco'}]
```

### 20)Affichez la config de la sous-interface g0/0.99 de chaque routeur en parcourant la liste des hosts de votre inventory.

```python
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
```

Résultat : 

```sh
R01
[{'interface': 'GigabitEthernet0/0.99', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.100.126'], 'prefix_length': ['26'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
R02
[{'interface': 'GigabitEthernet0/0.99', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.100.190'], 'prefix_length': ['26'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
R03
[{'interface': 'GigabitEthernet0/0.99', 'link_status': 'up', 'protocol_status': 'up', 'ip_address': ['172.16.100.254'], 'prefix_length': ['26'], 'vrf': '', 'mtu': '1500', 'ip_helper': [], 'outgoing_acl': '', 'inbound_acl': ''}]
```

### 21) déployez les configurations générées à la question 5 pour les routeurs et switchs des sites CPE-MARSEILLE et CPE-Paris. 
Pensez à sauvegarder vos implémentations avec la méthode save_config().

```python

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
```

on doit modifier le fichier hosts.json : 

```yaml
[
    {
        "hostname": "R01",
        "ip": "172.16.100.126",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "LYON" 
    },
    {
        "hostname": "R02",
        "ip": "172.16.100.190",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "MARSEILLE" 
    },
    {
        "hostname": "R03",
        "ip": "172.16.100.254",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "PARIS" 
    },
    {
        "hostname": "ESW1",
        "ip": "172.16.100.125",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "LYON" 
    },
    {
        "hostname": "ESW2",
        "ip": "172.16.100.189",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "MARSEILLE"     
    },
    {
        "hostname": "ESW3",
        "ip": "172.16.100.253",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "site" : "PARIS"   
    }
]
```

Résultat : 

Tous ce ping correctement

## Automatisation avec Napalm

pipenv install napalm

### Créer une connection 

```python
from napalm import get_network_driver
r01 = {
'hostname':'172.16.100.126',
'username': cisco,
'password': cisco
}
driver = get_network_driver('ios')
device = driver(**r01)
device.open()
```

### 26) Quel est la méthode de l’objet device permettant d’envoyer une commande show ? Exécutez la commande permettant de récupérerl’état des interfaces du routeur R1
 
```python
def question_26(device):
    device.open()
    output = device.cli(['show ip interface brief'])
    print(output)
    device.close()
    pass

```

Le résulat est : 

### 27) Quel est le format de sortie de la commande à la question précédente ? Quelle est la clé utilisée ?

La sortie est un dictionnaire. Sa clé est la commande rentré soit `show ip interface brie0`f et sa valeur la réponse avec les interfaces

```python
def question_27(device):
    print(type(output))
    pass

```

### 28) Quelle est la seconde méthode permettant de lire les données de configuration du routeur ? Affichez la table arp du routeur R1. Aidez-vous de la documentation napalm : NAPALM_doc

Pour afficher la table ARO, on peut utiliser get_arp_table()

```python
def question_28(device):
    device.open()
    output = device.get_arp_table()
    print(output)
    device.close()
    pass
```

résultat : 

### 29) Quel est le format de sortie de la commande à la question précédente ?

La sortie est au format d’une liste de dictionnaires.

```
def question_29(device):
    print(type(output))
    pass
```

### 30) Créez un fichier de config nommé loopback R01.conf dans le dossier config et copiez / collez le contenu suivant:

```conf
interface loopback 1
ip address 192.168.1.1 255.255.255.255
description "interface loopback 1"
no shut
interface loopback 2
ip address 192.168.2.1 255.255.255.255
description "interface loopback 2"
no shut
```

#### a) Déployez la configuration depuis le script napalm en utilisant la methode load_merge_candidate et en prenant soin d’afficher les changements apportés avant de commit votre config sur le routeur R1. AIdez-vous de la documentation napalm: Napalm doc

```python

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
```

Configuration de R1 avant déploiement : 

Configuration après déploiement :

#### b) Exécutez la commande show ip int brief sur le routeur R1 , que remarquez-vous sur la ligne des interfaces loopback 1 et loopback 2? Comment expliquer cette différence ?

Lookback 1 et 2 sont configurer avec NPAM donc par TFTP. Les autre sont configurer en NVRAM. On peut donc tracer les interface configurer avec npam et de façon plus classique. 

### 31) Créez le template jinja2 pour une configuration OSPF et la structure de données pour chaque routeur (R1, R2 et R3) permettant de générer la configuration du backbone OSPF en utilisant les données du tableau ci-dessous.

template/ospf.j2 

```j2
router ospf {{ ospf.process }}
router-id {{ ospf.id }}
{% for network in ospf.networks %}
    network {{ network.ip }} {{ network.wildmask }} area {{ network.area }}  
{% endfor %}
end
write

```


 data/ospf_r01.yaml :

 ```yaml

ospf:
  process: 1
  id: "1.1.1.1"
  networks:
    - ip: "172.16.10.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "10.1.3.0"
      wildmask: "0.0.0.3"
      area: "0"
    - ip: "10.1.1.0"
      wildmask: "0.0.0.3"
      area: "0"  
    - ip: "172.16.20.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "172.16.100.0"
      wildmask: "0.0.0.63"
      area: "0"
```

 data/ospf_r02.yaml :

 ```yaml
ospf:
  process: 1
  id: "2.2.2.2"
  networks:
    - ip: "172.16.30.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "172.16.40.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "172.16.100.64"
      wildmask: "0.0.0.63"
      area: "0"
    - ip: "10.1.2.0"
      wildmask: "0.0.0.3"
      area: "0"
    - ip: "10.1.1.0"
      wildmask: "0.0.0.3"
      area: "0" 
```


 data/ospf_r03.yaml :

 ```yaml

ospf:
  process: 1
  id: "3.3.3.3"
  networks:
    - ip: "172.16.50.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "172.16.60.0"
      wildmask: "0.0.0.255"
      area: "0"
    - ip: "172.16.100.192"
      wildmask: "0.0.0.63"
      area: "0"
    - ip: "10.1.2.0"
      wildmask: "0.0.0.3"
      area: "0"
    - ip: "10.1.3.0"
      wildmask: "0.0.0.3"
      area: "0" 
```

Génération des configurations : 

```python
def question_31():
    router_names = ['r01', 'r02', 'r03']
    for router_name in router_names:
        data = load_yaml_data_from_file(file_path=f'data/ospf_{router_name}.yaml')
        config = render_network_config(template_name='ospf.j2', data=data)
        save_built_config(f'config/ospf_{router_name}.config', config)
    pass
```

### 32) Déployez les configurations OSFP sur les routeurs R1, R2 et R3 (en une seule fois) depuis votre script python en utilisant les méthodes fournies par NAPALM. Pensez à sauvegarder vos déploiements

```python

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
```

résulat : 

### 33) A ce stade si votre configuration est correcte les machines de chaque site peuvent communiquer les unes avec les autres . Testez également le fonctionnement du routage inter-vlan entre les différents sites

Résulat : 

### 34) Développez une fonction permettant de créer un backup de chaque équipement réseau de l’infra à l’aide de la méthode get_config de napalm. Chaque backup devra être stocké dans le dossier config/backup

```python
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
```