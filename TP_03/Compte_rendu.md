# Compter rendu TP3

## 1.8 -Génération automatique de la configuration à l’aide de Jinja2

### 1) Développez l’ensemble des templates Jinja2 qui vous permettront de générer la configuration nécessaire pour le bon fonctionnement du bâtiment A. (Pour rappel, le vlan d’admin (99) est déjà configuré sur les équipements.) Les templates JInja2 doivent être sauvegardés dans le dossier templates.

Les templates sont déja disponibles dans le dossier templates 

### 2) Définissez les structures de données dans des fichiers JSON ou YAML (au choix) nécessaires pour remplir votre template JInja2 développé à la question 1. (Pour rappel, le vlan d’admin (99) est déjà configuré sur les équipements.) Les fichiers doivent être stockés dans le dossier data.

Les fichier de data en json snt déja fait dans le dossier data

### 3) Développez les fonctions vous permettant de générer automatiquement les configurations à partir du template Jinja2 et de la structure de données que vous avez définis à la question 1 et 2. Écrivez votre code dans le fichier scripts/create_config.py


```python

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

```

### 4) Développez les fonctions vous permettant de sauvegarder automatiquement les configurations générées à la question 3 dans le dossier config de votre workspace (TP03).

```python
def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass
```
Les fichiers de conf sont bien générés

### 5) Répétez les questions 1 à 4 pour le bâtiment B en vous appuyant sur les données du tableau ci-dessous

```python
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

```
Les fichiers de conf sont bien générés


## 1.9 -Automatisation réseau avec Nornir
`pipenv install nornir`

```python
from nornir import InitNornir
```

### 8) Créez un fichier config.yaml dans le dossier inventory de votre workspace et ajoutez la config suivant

fichier config.yaml
```yaml
inventory:
  plugin: SimpleInventory
  options:
    host_file: "inventory/hosts.yaml"
    group_file: "inventory/groups.yaml"
    defaults_file: "inventory/defaults.yaml"
runner:
  plugin: threaded
  options:
    num_workers: 20
```

### 9) Créez le fichier hosts.yaml dans le dossier inventory et ajoutez la structure de données suivante:

hosts.yaml:

```yaml
R1-CPE-BAT-A:
  hostname: 172.16.100.125
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: R1-CPE-BAT-A
    device_type: router
    device_model: C7200
    locality: lyon
    building: A

R2-CPE-BAT-A:
  hostname: 172.16.100.126
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: R2-CPE-BAT-A
    device_type: router
    device_model: C7200
    locality: lyon
    building: A

ESW1-CPE-BAT-A:
  hostname: 172.16.100.123
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: ESW1-CPE-BAT-A
    device_type: router_switch
    device_model: C3725
    locality: lyon
    building: A


R1-CPE-BAT-B:
  hostname: 172.16.100.189
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: R1-CPE-BAT-B
    device_type: router
    device_model: C7200
    locality: lyon
    building: B

R2-CPE-BAT-B:
  hostname: 172.16.100.190
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: R2-CPE-BAT-B
    device_type: router
    device_model: C7200
    locality: lyon
    building: B

ESW1-CPE-BAT-B:
  hostname: 172.16.100.187
  port: 22
  groups:
    - ios
  data: # Anything under this key is custom data
    device_name: ESW1-CPE-BAT-B
    device_type: router_switch
    device_model: C3725
    locality: lyon
    building: B
```

### 10) Créez le fichier groups.yaml dans le dossier inventory et ajoutez la structure de données suivante:

groups.yaml :

```yaml
ios:
  platform: ios
  data:
    vendor: Cisco
```

### 11) Créez le fichier defaults.yaml dans le dossier inventory et ajoutez la structure de données suivante:

defaults.yaml :

```yaml
username: cisco
password: cisco
```

### 12) Vous pouvez à présent initialiser Nornir dans le __main__ du script run_nornir.py de la manière suivante :

```python
if __name__ == "__main__":
    nr = InitNornir(config_file="inventory/config.yaml")
```

### 13) Quels sont les attributs de l’objet nr ? Pour connaître les attributs de l’objet nr utilisez l’attribut __dict__ (utilisable sur tout objet python). Quel est le format de données de sortie ? Quelles sont les attributs de l’objet nr ? A votre avis lequel nous permettrait d’aller lire l’inventaire que nous avons précédemment défini (question 9) ?

```python
def question_13(nr):
    print(nr.__dict__)
    print(type(nr.__dict__))
    pass
```

résulat :

```sh
{'data': <nornir.core.state.GlobalState object at 0x7ff6dc631f70>, 'inventory': <nornir.core.inventory.Inventory object at 0x7ff6dc019e00>, 'config': <nornir.core.configuration.Config object at 0x7ff6dbcdcbd0>, 'processors': [], 'runner': <nornir.plugins.runners.ThreadedRunner object at 0x7ff6dc2a79d0>}
<class 'dict'>
```

Les attributs de l'objet sont data, inventory, processors et runner.
Le format de sortie est un dictionnaire.
L'attribut qui nous permt d'aller lire dans l'inventaire est inventory

### 14) Affichez l’attribut hosts de l’attribut que vous avez trouvé à la question 13. Quelles sont les données retournées ? Quel est le format de données retourné 

```python
def question_14(nr):
    print(nr.inventory.hosts)
    print(type(nr.inventory.hosts))
    pass
```
résultat : 

```sh
{'R1-CPE-BAT-A': Host: R1-CPE-BAT-A, 'R2-CPE-BAT-A': Host: R2-CPE-BAT-A, 'ESW1-CPE-BAT-A': Host: ESW1-CPE-BAT-A, 'R1-CPE-BAT-B': Host: R1-CPE-BAT-B, 'R2-CPE-BAT-B': Host: R2-CPE-BAT-B, 'ESW1-CPE-BAT-B': Host: ESW1-CPE-BAT-B}
<class 'nornir.core.inventory.Hosts'>
```
Les données retournés sont la list des hosts
C'est encore un dictionnaire

### 15) Affichez la valeur du premier élément de l’objet à la question 14. Quelle est la valeur retournée ? Quel est le type de cette valeur (fonction type() )?

```python
def question_15(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A'))
    print(type(nr.inventory.hosts.get('R1-CPE-BAT-A')))
    pass
```

résultat: 

```sh
R1-CPE-BAT-A
<class 'nornir.core.inventory.Host'>
```

la valeur retrouné est son nom et c'est un object

### 16) Utilisez la méthode dir() sur l’objet de la question 15. Parmis les attributs affichés, lequel permet d’afficher l’adresse ip et le username / password du host en question? Affichez les valeurs de ces attributs dans la console. Depuis quel fichier ces données ont été récupérées ? Dans quelle section de ce fichier plus précisément?


```python
def question_16(nr):
    print(dir(nr.inventory.hosts.get('R1-CPE-BAT-A')))
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').hostname)
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').username)
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').password)
    pass
```

résultat : 
```sh
['__bool__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_get_connection_options_recursively', '_has_parent_group_by_name', '_has_parent_group_by_object', 'close_connection', 'close_connections', 'connection_options', 'connections', 'data', 'defaults', 'dict', 'extended_data', 'extended_groups', 'get', 'get_connection', 'get_connection_parameters', 'groups', 'has_parent_group', 'hostname', 'items', 'keys', 'name', 'open_connection', 'password', 'platform', 'port', 'schema', 'username', 'values']
172.16.100.125
cisco
cisco
```

l'attribut permettant d'affiché :
    - l’adresse ip est hostname. Les données ont été récupérées du fichier hosts.yaml
    - username est username. Les données ont été récupérées du fichier defaults.yaml
    - password est password. Les données ont été récupérées du fichier defaults.yaml

Le point d'entré des fichiers est le fichier hosts.yaml. La section de R1-CPE-BAT-A. Les data-données sont dans le section data. 

### 17) Ajoutez une nouvelle entrée à la section de ce fichier, par exemple: room: 001 et exécuter de nouveau le script.

```yaml
R1-CPE-BAT-A:
  hostname: 172.16.100.125
  port: 22
  groups:
    - 0
  data: # Anything under this key is custom data
    device_name: R1-CPE-BAT-A
    device_type: router
    device_model: C7200
    locality: lyon
    building: A
    room: '001'
```

### 18) Affichez la valeur de l’attribut “room“ crée à la question 17 sur le terminal

```python
def question_18(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').data['room'])
    pass
```

résultat : 
```sh
001
```

### 19) Nornir nous fournit également la possibilité d’accéder aux données du fichier groups.yaml à l’aide de l’attribut groups de l’objet inventory. Affichez les groupes définis dans le fichier groups.yaml à l’aide du code suivant:


```python
def question_19(nr):
    print(nr.inventory.groups)
    pass
```

résultat : 
```sh
{'ios': Group: ios}
```

### 20) Il est possible d’afficher les groupes rattaché à un host à l’aide de l’attribut groups de l’objet:

```python
def question_20(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups)
    pass

```

résultat :
```sh
[Group: ios]
```

### 21) Par exemple, si on veut afficher les keys définis dans le fichier groups.yaml du host RP1-CPE-BAT-A  il suffit d'exécuter : 

```python
def question_21(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].keys())
    pass
```

resultat :
```sh
dict_keys(['vendor'])
```

### 22) Affichez le vendor du host R1-CPE-BAT-A en partant du code de la question 21

```python
def question_22(nr):
    print(nr.inventory.hosts.get('R1-CPE-BAT-A').groups[0].values())
    pass
```

résultat :

```sh
dict_values(['Cisco'])

```

### 23) Affichez le hostname (adresse ip) de chaque host définis dans le fichier hosts.yaml en utilisant l’objet nr définis à la question 12. Aidez-vous des questions précédentes.

```python
def question_23(nr):
    for i in nr.inventory.hosts :
        print(nr.inventory.hosts.get(str(i)).hostname)
    pass
```

résultat : 

```sh
172.16.100.125
172.16.100.126
172.16.100.123
172.16.100.189
172.16.100.190
172.16.100.187
```

### 24) Nornir nous donne la possibilité d’appliquer des filtres sur notre inventory pour récupérer par exemple un host à partir de son hostname par exemple. A l’aide du code suivant affichez la liste des hosts de type router.

```python
def question_24(nr):
    print(nr.filter(device_type="router").inventory.hosts.keys())
    pass
```

résultat : 
```sh
dict_keys(['R1-CPE-BAT-A', 'R2-CPE-BAT-A', 'R1-CPE-BAT-B', 'R2-CPE-BAT-B'])
```

### 25) Affichez à présent la liste des hosts de type router_switch.

```python
def question_25(nr):
    print(nr.filter(device_type="router_switch").inventory.hosts.keys())
    pass
```

résultat : 
```sh
dict_keys(['ESW1-CPE-BAT-A', 'ESW1-CPE-BAT-B'])
```

### 26) Importez les classes Task et Result et définissez une première task nommée hello_world 

```python
from nornir.core.task import Task, Result
def hello_world(task: Task) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
    )

def question_26(nr):
    result = nr.run(task=hello_world)
    print(result)
    pass
```

résultat : 
```sh
AggregatedResult (hello_world): {'R1-CPE-BAT-A': MultiResult: [Result: "hello_world"], 'R2-CPE-BAT-A': MultiResult: [Result: "hello_world"], 'ESW1-CPE-BAT-A': MultiResult: [Result: "hello_world"], 'R1-CPE-BAT-B': MultiResult: [Result: "hello_world"], 'R2-CPE-BAT-B': MultiResult: [Result: "hello_world"], 'ESW1-CPE-BAT-B': MultiResult: [Result: "hello_world"]}
```

### 27) Que retourne la variable result à la question 27 ? Aidez-vous de la méthode type()

```python
def question_27(nr):
    result = nr.run(task=hello_world)
    print(type(result))
    pass
```

résultat : 
```sh
<class 'nornir.core.task.AggregatedResult'>
```
 La varaible retourne un object nornir.core.task.AggregatedResult 

### 28) Nornir fournit une fonction print_result qui permet d’afficher des logs sur les événements retournés par la task. Utilisez print_result pour afficher la variable result.

```python
pipenv install nornir_utils
from nornir_utils.plugins.functions import print_result

def question_29(nr):
    result = nr.run(task=hello_world)
    print(print_result(result))
    pass
```
résultat : 

```sh
hello_world*********************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
ESW1-CPE-BAT-A says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
ESW1-CPE-BAT-B says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-A ** changed : False **********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
R1-CPE-BAT-A says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-B ** changed : False **********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
R1-CPE-BAT-B says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-A ** changed : False **********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
R2-CPE-BAT-A says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-B ** changed : False **********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
R2-CPE-BAT-B says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
None
```
### 29) Après avoir affiché result à l’aide de la fonction print_result, qu’avez-vous remarqué ? Sur quel équipement la task s’est exécutée par défaut ?

Par défaut, la task s'execute sur tous les équipements. Cependant aucun équipement n'a eu de changement car le changed : False


### 30) Faites en sorte que la task hello_world s’exécute uniquement sur les équipements de type router_switch.

```python
def question_30(nr):
    router_switch = nr.filter(device_type="router_switch")
    result = router_switch.run(task=hello_world)
    print(print_result(result))
    pass
```

résultat: 
```sh
hello_world*********************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
ESW1-CPE-BAT-A says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv hello_world ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
ESW1-CPE-BAT-B says hello world!
^^^^ END hello_world ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 31) Installez les packages nornir_napalm et nornir_netmiko à votre environnement de développement (TP03):

```sh
pipenv install nornir_napalm
pipenv install nornir_netmiko
```
Importez les méthodes de chaque package:

```python
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command, netmiko_save_config, netmiko_commit
```

### 32) Développez une task permettant d’afficher l’état des interfaces de chaque routeur à l’aide de la fonction napalm_cli.

```python
def question_32(nr):
    router = nr.filter(device_type="router")
    result = nr.run(task=napalm_cli, commands=["sh ip int br"])
    print_result(result)
    pass
```

résultat : 

```sh
(reseau-etendu-6MQWliMz) cpe@cpe-VirtualBox:~/LEA/reseau-etendu/TP_03$ python3 -m scripts.run_nornir
napalm_cli**********************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'FastEthernet0/1            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'FastEthernet1/0            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/1            unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/2            unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/3            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/4            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/5            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/6            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/7            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/8            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/9            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/10           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/11           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/12           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/13           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/14           unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/15           unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet2/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Vlan1                      unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'Vlan99                     172.16.100.123  YES NVRAM  '
                  'up                    up      \n'
                  'Loopback1                  unassigned      YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'FastEthernet0/1            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'FastEthernet1/0            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/1            unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/2            unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/3            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/4            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/5            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/6            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/7            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/8            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/9            unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/10           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/11           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/12           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/13           unassigned      YES unset  '
                  'up                    down    \n'
                  'FastEthernet1/14           unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet1/15           unassigned      YES unset  '
                  'up                    up      \n'
                  'FastEthernet2/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Vlan1                      unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'Vlan99                     172.16.100.187  YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            172.16.100.62   YES NVRAM  '
                  'up                    up      \n'
                  'Serial1/0                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/1                  10.1.1.1        YES NVRAM  '
                  'up                    up      \n'
                  'Serial1/2                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'GigabitEthernet2/0         unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.10      172.16.10.253   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.20      172.16.20.253   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.99      172.16.100.125  YES NVRAM  '
                  'up                    up      \n'
                  'Loopback1                  1.1.1.1         YES NVRAM  '
                  'up                    up      \n'
                  'Loopback2                  1.1.1.2         YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/0                  10.103.1.1      YES NVRAM  '
                  'up                    down    \n'
                  'Serial1/1                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/2                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/0                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/1                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/2                  10.1.5.2        YES NVRAM  '
                  'up                    up      \n'
                  'Serial2/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'GigabitEthernet3/0         unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.10      172.16.30.253   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.20      172.16.40.253   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.99      172.16.100.189  YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/0                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/1                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/2                  10.1.2.1        YES NVRAM  '
                  'up                    up      \n'
                  'Serial1/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'GigabitEthernet2/0         unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.10      172.16.10.254   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.20      172.16.20.254   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet2/0.99      172.16.100.126  YES NVRAM  '
                  'up                    up      \n'
                  'Loopback1                  2.2.2.2         YES NVRAM  '
                  'up                    up      \n'
                  'Loopback2                  2.2.2.3         YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'sh ip int br': 'Interface                  IP-Address      OK? Method '
                  'Status                Protocol\n'
                  'FastEthernet0/0            unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/0                  10.102.1.1      YES NVRAM  '
                  'up                    down    \n'
                  'Serial1/1                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/2                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial1/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/0                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/1                  10.1.4.2        YES NVRAM  '
                  'up                    up      \n'
                  'Serial2/2                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'Serial2/3                  unassigned      YES NVRAM  '
                  'administratively down down    \n'
                  'GigabitEthernet3/0         unassigned      YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.10      172.16.30.254   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.20      172.16.40.254   YES NVRAM  '
                  'up                    up      \n'
                  'GigabitEthernet3/0.99      172.16.100.190  YES NVRAM  '
                  'up                    up'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 33) Développez une task permettant d’afficher la table arp de chaque switch référencé dans l’inventory. Utilisez la fonction napalm_get pour cela.


```python
def question_33(nr):
    router_switch = nr.filter(device_type="router_switch")
    result = nr.run(task=napalm_get, getters=["arp_table"])
    print_result(result)
    pass
```

Résulat : 
```sh
(reseau-etendu-6MQWliMz) cpe@cpe-VirtualBox:~/LEA/reseau-etendu/TP_03$ python3 -m scripts.run_nornir
napalm_get**********************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': 1.0,
                   'interface': 'Vlan99',
                   'ip': '172.16.100.2',
                   'mac': '00:00:5E:00:01:63'},
                 { 'age': -1.0,
                   'interface': 'Vlan99',
                   'ip': '172.16.100.123',
                   'mac': 'C2:02:0F:B5:00:00'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': 1.0,
                   'interface': 'Vlan99',
                   'ip': '172.16.100.2',
                   'mac': '00:00:5E:00:01:63'},
                 { 'age': -1.0,
                   'interface': 'Vlan99',
                   'ip': '172.16.100.187',
                   'mac': 'C2:04:12:25:00:00'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.10',
                   'ip': '172.16.10.253',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet2/0.10',
                   'ip': '172.16.10.254',
                   'mac': 'CA:03:69:82:00:38'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.20',
                   'ip': '172.16.20.253',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet2/0.20',
                   'ip': '172.16.20.254',
                   'mac': 'CA:03:69:82:00:38'},
                 { 'age': 3.0,
                   'interface': 'FastEthernet0/0',
                   'ip': '172.16.100.2',
                   'mac': '08:00:27:F6:B8:64'},
                 { 'age': -1.0,
                   'interface': 'FastEthernet0/0',
                   'ip': '172.16.100.62',
                   'mac': 'CA:01:69:6A:00:00'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.123',
                   'mac': 'C2:02:0F:B5:00:00'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.125',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.126',
                   'mac': 'CA:03:69:82:00:38'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.10',
                   'ip': '172.16.30.253',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet3/0.10',
                   'ip': '172.16.30.254',
                   'mac': 'CA:07:69:B7:00:54'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.20',
                   'ip': '172.16.40.253',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet3/0.20',
                   'ip': '172.16.40.254',
                   'mac': 'CA:07:69:B7:00:54'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.187',
                   'mac': 'C2:04:12:25:00:00'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.189',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.190',
                   'mac': 'CA:07:69:B7:00:54'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.10',
                   'ip': '172.16.10.252',
                   'mac': '00:00:5E:00:01:0A'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet2/0.10',
                   'ip': '172.16.10.253',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.10',
                   'ip': '172.16.10.254',
                   'mac': 'CA:03:69:82:00:38'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.20',
                   'ip': '172.16.20.252',
                   'mac': '00:00:5E:00:01:14'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet2/0.20',
                   'ip': '172.16.20.253',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.20',
                   'ip': '172.16.20.254',
                   'mac': 'CA:03:69:82:00:38'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.123',
                   'mac': 'C2:02:0F:B5:00:00'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.124',
                   'mac': '00:00:5E:00:01:63'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.125',
                   'mac': 'CA:01:69:6A:00:38'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet2/0.99',
                   'ip': '172.16.100.126',
                   'mac': 'CA:03:69:82:00:38'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.10',
                   'ip': '172.16.30.252',
                   'mac': '00:00:5E:00:01:0A'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet3/0.10',
                   'ip': '172.16.30.253',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.10',
                   'ip': '172.16.30.254',
                   'mac': 'CA:07:69:B7:00:54'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.20',
                   'ip': '172.16.40.252',
                   'mac': '00:00:5E:00:01:14'},
                 { 'age': 52.0,
                   'interface': 'GigabitEthernet3/0.20',
                   'ip': '172.16.40.253',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.20',
                   'ip': '172.16.40.254',
                   'mac': 'CA:07:69:B7:00:54'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.187',
                   'mac': 'C2:04:12:25:00:00'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.188',
                   'mac': '00:00:5E:00:01:63'},
                 { 'age': 3.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.189',
                   'mac': 'CA:06:69:A0:00:54'},
                 { 'age': -1.0,
                   'interface': 'GigabitEthernet3/0.99',
                   'ip': '172.16.100.190',
                   'mac': 'CA:07:69:B7:00:54'}]}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 34) Développez deux tasks permettant de créer une interface de loopback sur les routeurs R1 et R2 du bâtiment A . (Une task par routeur) à l’aide de la task napalm_configure

interface loopback 1 R1: 1.1.1.1 255.255.255.255
interface loopback 1 R2: 2.2.2.2 255.255.255.255

```python
def question_34(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=napalm_configure, configuration="int lo1\nip address 1.1.1.1 255.255.255.255")
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=napalm_configure, configuration="int lo1\nip address 2.2.2.2 255.255.255.255")
    print_result(result)

    pass
```

Résultat : 

```sh
napalm_configure****************************************************************
* R1-CPE-BAT-A ** changed : True ***********************************************
vvvv napalm_configure ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
+int lo1
+ip address 1.1.1.1 255.255.255.255end
^^^^ END napalm_configure ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
napalm_configure****************************************************************
* R2-CPE-BAT-A ** changed : True ***********************************************
vvvv napalm_configure ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
+int lo1
+ip address 2.2.2.2 255.255.255.255end
^^^^ END napalm_configure ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 35) Développez une fonction contenant une task permettant de sauvegarder la running-config sur les équipements (routeurs / switchs) depuis napalm_cli.

```python
def question_35(nr):
    result = nr.run(task=napalm_cli, commands=["wr"] ) 
    print_result(result)
    pass
```

Résultat : 
```sh
(reseau-etendu-6MQWliMz) cpe@cpe-VirtualBox:~/LEA/reseau-etendu/TP_03$ python3 -m scripts.run_nornir
napalm_cli**********************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-A ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-B ** changed : False **********************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{'wr': 'Building configuration...\n[OK]'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 36) Développez une fonction permettant d’afficher l’état des interfaces de chaque routeur à l’aide de la task netmiko_send_command.

```python
def question_36(nr):
    router = nr.filter(device_type="router")
    result = nr.run(task=netmiko_send_command, command_string="sh ip int brief")
    print_result(result)

    pass
```

Résultat : 

```sh

(reseau-etendu-6MQWliMz) cpe@cpe-VirtualBox:~/LEA/reseau-etendu/TP_03$ python3 -m scripts.run_nornir
netmiko_send_command************************************************************
* ESW1-CPE-BAT-A ** changed : False ********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  up                    up      
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
FastEthernet1/0            unassigned      YES unset  up                    down    
FastEthernet1/1            unassigned      YES unset  up                    up      
FastEthernet1/2            unassigned      YES unset  up                    up      
FastEthernet1/3            unassigned      YES unset  up                    down    
FastEthernet1/4            unassigned      YES unset  up                    down    
FastEthernet1/5            unassigned      YES unset  up                    down    
FastEthernet1/6            unassigned      YES unset  up                    down    
FastEthernet1/7            unassigned      YES unset  up                    down    
FastEthernet1/8            unassigned      YES unset  up                    down    
FastEthernet1/9            unassigned      YES unset  up                    down    
FastEthernet1/10           unassigned      YES unset  up                    down    
FastEthernet1/11           unassigned      YES unset  up                    down    
FastEthernet1/12           unassigned      YES unset  up                    down    
FastEthernet1/13           unassigned      YES unset  up                    down    
FastEthernet1/14           unassigned      YES unset  up                    up      
FastEthernet1/15           unassigned      YES unset  up                    up      
FastEthernet2/0            unassigned      YES NVRAM  administratively down down    
Vlan1                      unassigned      YES NVRAM  up                    up      
Vlan99                     172.16.100.123  YES NVRAM  up                    up      
Loopback1                  unassigned      YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ESW1-CPE-BAT-B ** changed : False ********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  administratively down down    
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
FastEthernet1/0            unassigned      YES unset  up                    down    
FastEthernet1/1            unassigned      YES unset  up                    up      
FastEthernet1/2            unassigned      YES unset  up                    up      
FastEthernet1/3            unassigned      YES unset  up                    down    
FastEthernet1/4            unassigned      YES unset  up                    down    
FastEthernet1/5            unassigned      YES unset  up                    down    
FastEthernet1/6            unassigned      YES unset  up                    down    
FastEthernet1/7            unassigned      YES unset  up                    down    
FastEthernet1/8            unassigned      YES unset  up                    down    
FastEthernet1/9            unassigned      YES unset  up                    down    
FastEthernet1/10           unassigned      YES unset  up                    down    
FastEthernet1/11           unassigned      YES unset  up                    down    
FastEthernet1/12           unassigned      YES unset  up                    down    
FastEthernet1/13           unassigned      YES unset  up                    down    
FastEthernet1/14           unassigned      YES unset  up                    up      
FastEthernet1/15           unassigned      YES unset  up                    up      
FastEthernet2/0            unassigned      YES NVRAM  administratively down down    
Vlan1                      unassigned      YES NVRAM  up                    up      
Vlan99                     172.16.100.187  YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-A ** changed : False **********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            172.16.100.62   YES NVRAM  up                    up      
Serial1/0                  unassigned      YES NVRAM  administratively down down    
Serial1/1                  10.1.1.1        YES NVRAM  up                    up      
Serial1/2                  unassigned      YES NVRAM  administratively down down    
Serial1/3                  unassigned      YES NVRAM  administratively down down    
GigabitEthernet2/0         unassigned      YES NVRAM  up                    up      
GigabitEthernet2/0.10      172.16.10.253   YES NVRAM  up                    up      
GigabitEthernet2/0.20      172.16.20.253   YES NVRAM  up                    up      
GigabitEthernet2/0.99      172.16.100.125  YES NVRAM  up                    up      
Loopback1                  1.1.1.1         YES TFTP   up                    up      
Loopback2                  1.1.1.2         YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R1-CPE-BAT-B ** changed : False **********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  administratively down down    
Serial1/0                  10.103.1.1      YES NVRAM  up                    down    
Serial1/1                  unassigned      YES NVRAM  administratively down down    
Serial1/2                  unassigned      YES NVRAM  administratively down down    
Serial1/3                  unassigned      YES NVRAM  administratively down down    
Serial2/0                  unassigned      YES NVRAM  administratively down down    
Serial2/1                  unassigned      YES NVRAM  administratively down down    
Serial2/2                  10.1.5.2        YES NVRAM  up                    up      
Serial2/3                  unassigned      YES NVRAM  administratively down down    
GigabitEthernet3/0         unassigned      YES NVRAM  up                    up      
GigabitEthernet3/0.10      172.16.30.253   YES NVRAM  up                    up      
GigabitEthernet3/0.20      172.16.40.253   YES NVRAM  up                    up      
GigabitEthernet3/0.99      172.16.100.189  YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-A ** changed : False **********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  administratively down down    
Serial1/0                  unassigned      YES NVRAM  administratively down down    
Serial1/1                  unassigned      YES NVRAM  administratively down down    
Serial1/2                  10.1.2.1        YES NVRAM  up                    up      
Serial1/3                  unassigned      YES NVRAM  administratively down down    
GigabitEthernet2/0         unassigned      YES NVRAM  up                    up      
GigabitEthernet2/0.10      172.16.10.254   YES NVRAM  up                    up      
GigabitEthernet2/0.20      172.16.20.254   YES NVRAM  up                    up      
GigabitEthernet2/0.99      172.16.100.126  YES NVRAM  up                    up      
Loopback1                  2.2.2.2         YES TFTP   up                    up      
Loopback2                  2.2.2.3         YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* R2-CPE-BAT-B ** changed : False **********************************************
vvvv netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  administratively down down    
Serial1/0                  10.102.1.1      YES NVRAM  up                    down    
Serial1/1                  unassigned      YES NVRAM  administratively down down    
Serial1/2                  unassigned      YES NVRAM  administratively down down    
Serial1/3                  unassigned      YES NVRAM  administratively down down    
Serial2/0                  unassigned      YES NVRAM  administratively down down    
Serial2/1                  10.1.4.2        YES NVRAM  up                    up      
Serial2/2                  unassigned      YES NVRAM  administratively down down    
Serial2/3                  unassigned      YES NVRAM  administratively down down    
GigabitEthernet3/0         unassigned      YES NVRAM  up                    up      
GigabitEthernet3/0.10      172.16.30.254   YES NVRAM  up                    up      
GigabitEthernet3/0.20      172.16.40.254   YES NVRAM  up                    up      
GigabitEthernet3/0.99      172.16.100.190  YES NVRAM  up                    up      
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

```

### 37) Développez une fonction permettant de créer une interface de loopback 2 sur les routeurs R1 et R2 du bâtiment A . (Une task par routeur) en utilisant la task netmiko_send_config

interface loopback 2 R1: 1.1.1.2 255.255.255.255
interface loopback 2 R2: 2.2.2.3 255.255.255.255

```python
def question_37(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=netmiko_send_config, config_commands=["int lo2","ip address 1.1.1.2 255.255.255.255"])
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=netmiko_send_config, config_commands=["int lo2","ip address 2.2.2.3 255.255.255.255"])
    print_result(result)
    pass
```
Résultat : 

```sh
netmiko_send_config*************************************************************
* R1-CPE-BAT-A ** changed : True ***********************************************
vvvv netmiko_send_config ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R1-CPE-BAT-A(config)#int lo2
R1-CPE-BAT-A(config-if)#ip address 1.1.1.2 255.255.255.255
R1-CPE-BAT-A(config-if)#end
R1-CPE-BAT-A#
^^^^ END netmiko_send_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
netmiko_send_config*************************************************************
* R2-CPE-BAT-A ** changed : True ***********************************************
vvvv netmiko_send_config ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R2-CPE-BAT-A(config)#int lo2
R2-CPE-BAT-A(config-if)#ip address 2.2.2.3 255.255.255.255
R2-CPE-BAT-A(config-if)#end
R2-CPE-BAT-A#
^^^^ END netmiko_send_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

### 38) Développez une fonction contenant une task permettant de sauvegarder la running-config de la question précédente à l’aide de la task netmiko_save_config

```python
def question_38(nr):
    result = nr.filter(device_name="R1-CPE-BAT-A").run(task=netmiko_save_config)
    print_result(result)
    result = nr.filter(device_name="R2-CPE-BAT-A").run(task=netmiko_save_config)
    print_result(result)
    pass
```

Résultat : 

```sh
netmiko_save_config*************************************************************
* R1-CPE-BAT-A ** changed : True ***********************************************
vvvv netmiko_save_config ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
write mem
Building configuration...
[OK]
R1-CPE-BAT-A#
^^^^ END netmiko_save_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
netmiko_save_config*************************************************************
* R2-CPE-BAT-A ** changed : True ***********************************************
vvvv netmiko_save_config ** changed : True vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
write mem
Building configuration...
[OK]
R2-CPE-BAT-A#
^^^^ END netmiko_save_config ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
