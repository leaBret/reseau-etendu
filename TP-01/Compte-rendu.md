# Compte rendu TP1 Automatisation réseau 

## Préparations des variables  

### 1) Quels sont les éléments de configuration à réaliser pour que les équipements du vlan 10 et du vlan 20 du bâtiment C puissent communiquer ? 

Il y a plusieurs éléments :  
Le switch ESW2:  

- Interface f1/1 en mode access vlan 10 
- Interface f 1/2  en mode access vlan 20
- Interface f 1/0 en mode trunk avec les vlan autorisé

Le routeur R2:  
- Créer les sous-interfaces G0/0.10 et G0/0.20 

### 2) Parmi les éléments de configuration identifiés à la question 1, quelles sont les variables Jinja que vous avez pu identifier ? 

Les variables identifiées sont 
- interface
- id de vlan
- mode du vlan
- adresse ip
- netmask 

### 3) Définissez une structure de données JSON pour recenser les variables identifiées ainsi que leurs valeurs. Créez les fichiers R2.json et ESW2.json dans le dossier data. 

 
Pour le fichier R2.json :  

 ```json
 {
    "interfaces":
    [
        {
            "name":"G0/0.10",
            "description":"Gateway for vlan 10",
            "vlan_id":"10",
            "ip":"172.16.30.254",
            "masque":"255.255.255.0"

        },
        {
            "name":"G0/0.20",
            "description":"Gateway for vlan 20",
            "vlan_id":"20",
            "ip":"172.16.40.254",
            "masque":"255.255.255.0"
        }
    ]
}

 ```

 

Pour le fichier ESW2.json : 

 ```json
{
    "vlans":
    [
        {
            "name":"vlan10",
            "id":"10"
        },
        {
            "name":"vlan20",
            "id":"20"
        }
    ],
    "interfaces":
    [
        {
            "name":"f1/1",
            "vlan_mode":"access",
            "vlan_id":"10"

        },
        {
            "name":"f1/2",
            "vlan_mode":"access",
            "vlan_id":"20"
        },
        {
            "name":"f1/0",
            "vlan_mode":"trunk",
            "vlan_allowed":["10","20"]
        }
    ]
}

```


## 1.7 Développer la fonction python permettant de lire les données définis dans les fichiers json 

 

Commande pour exécuter le script en mode “module” :

```sh
python3 -m scripts.__main__  
```
 

Fonction pour load_json_data_from_file :

```python

def load_json_data_from_file(file_path):
    with open(file_path) as json_file:
        data=json.load(json_file)
    return data
```

Si le chemin n’est pas bon, on a une erreur du type :  

```python
FileNotFoundError: [Errno 2] No such file or directory: 'data/R2.jsonr' 
```

 

Pour gérer les exceptions :  

 ```python

def load_json_data_from_file(file_path):
    try:
        with open(file_path) as json_file:
            data=json.load(json_file)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found",e)
    pass

```


## 1.8 -Définition des templates Jinja  

 
Template R2.j2 : 

```sh

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

```

Template ESW2.j2 :  

 ```sh
{% for vlan in vlans %}
vlan {{ vlan.id }}
name {{ vlan.name }}
{% endfor %}

{% for interface in interfaces %}

{% if interface.vlan_mode == "trunk" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport trunk allowed vlan {{ interface.vlan_allowed|join(', ')  }}
{% endif %}

{% if interface.vlan_mode == "access" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport access vlan {{ interface.vlan_id }}
{% endif %}

no shutdown
exit
{% endfor %}


```

## 1.9- Génération automatique de la configuration réseau 

 
Installer jinja : 

```sh 
pipenv install Jinja2 
```

Compléter la fonction render_network-config:  

```python
 def render_network_config(template_name, data):

    template = env.get_template(template_name)
    print(template.render(data))
    return template.render(data) 
    pass
```

Développer la fonction save_build_config  :  
 
```python
def save_built_config(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    pass

```

La fonction main : 

```python

if __name__ == "__main__":

    #process R2
    r2_data = load_json_data_from_file(file_path='data/R2.json')
    r2_config = render_network_config(template_name='R2.j2', data=r2_data)
    save_built_config('config/R2.conf', r2_config)

    #process ESW2
    esw2_data = load_json_data_from_file(file_path='data/ESW2.json')
    esw2_config = render_network_config(template_name='ESW2.j2', data=esw2_data)
    save_built_config('config/ESW2.conf', esw2_config)
    
```


Les fichiers de conf sont bien généré dans le dossier config  

Après avoir copié les fichiers de config dans le routeur et le switch, les deux ordinateurs appartenant à des vlans différents communiquent bien entre eux.

## 1.10 - Ajout d’un nouveau bâtiment D à l’architecture

Reprenez le jeu de données JSON défini dans vos fichiers R2.json et ESW2.json et créez les jeux de données en YAML dans les fichiers R2.yaml et ESW4.yaml avec les données du tableau précédent.

pour ESW4.json: 

```yaml

vlans:
  - name: vlan10
    id: 10
  - name: vlan20
    id: 20
  - name: vlan99
    id: 99

interfaces:
  - name: f1/1
    vlan_mode: access
    vlan_id: 10
  - name: f1/2
    vlan_mode: access
    vlan_id: 20
  - name: f1/0
    vlan_mode: trunk
    vlan_allowed:
      - 10
      - 20
      - 99
  - name: vlan99
    ip: 172.16.100.253
    masque: 255.255.255.192

```

pour r2.yaml :

```yaml
interfaces:
  - name: "G2/0.10"
    description: "Gateway for vlan 10"
    vlan_id: "10"
    ip: "172.16.50.254"
    masque: "255.255.255.0"

  - name: "G2/0.20"
    description: "Gateway for vlan 20"
    vlan_id: "20"
    ip: "172.16.60.254"
    masque: "255.255.255.0"

  - name: "G2/0.99"
    description: "Gateway for vlan 99"
    vlan_id: "20"
    ip: "172.16.100.254"
    masque: "255.255.255.192"
```

### Créer une fonction permettant de retourner automatiquement le contenu des fichiers R2.yaml et ESW4.yaml

```python
def load_yaml_data_from_file(file_path):
    try:
        with open(file_path) as yaml_file:
            data = yaml.safe_load(yaml_file)
            print(data)
        return data
    except FileNotFoundError as e: 
        print("Erreur, file path not found", e)

```

À la sortie de la fonction, les données sont dans le format d'une liste contenant des dictionnaires.

Il n'est pas utile de modifier le template jinja de R2 car il est déja suffisament configuré pour prendre en compte toute les nouvelle monification. Peut si les vairiables sont  en yaml ou en jinja, la fonction transforme les données en une liste contenant des dictionnaires. 

Il faut juste modifier le template de SW4 car le jinja ne permet pas de mettre une adresse ip

```sh
{% for vlan in vlans %}
vlan {{ vlan.id }}
name {{ vlan.name }}
{% endfor %}

{% for interface in interfaces %}

{% if interface.vlan_mode == "trunk" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport trunk allowed vlan {{ interface.vlan_allowed|join(', ')  }}
{% endif %}

{% if interface.vlan_mode == "access" %}
interface {{ interface.name }}
switchport mode {{ interface.vlan_mode }}
switchport access vlan {{ interface.vlan_id }}
{% endif %}

no shutdown
exit
{% endfor %}

```

Les configurations générées ont pu être correctement appliquées.