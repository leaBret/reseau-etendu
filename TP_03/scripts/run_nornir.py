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
    pass
 
def question_33(nr):
    pass

def question_34(nr):
    pass

def question_35(nr):
    pass

def question_36(nr):
    pass

def question_37(nr):
    pass

def question_38(nr):
    pass

def question_39(nr):
    pass

def question_39_d(nr):
    pass

def question_40(nr):
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
    question_30(nr)

    #question_32(nr)
    #question_33(nr)
    #question_34(nr)
    #question_35(nr)
    #question_36(nr)
    #question_37(nr)
    #question_38(nr)
    #question_39(nr)
    #question_39_d(nr)

    #question_40(nr)
    pass
