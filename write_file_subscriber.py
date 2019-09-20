import redis
import os

r = redis.Redis()

def write_to_disk():
    configs = r.hgetall('primary_network')
    output_template = """#Configuration
    
DEVICE=enp3s0
ONBOOT=yes
IPADDR={}
NETMASK={}
GATEWAY={}
DNS1={}
DNS2={}"""

    output = output_template.format(configs['ip_address']
            , config['netmask']
            , config['gateway']
            , config['nameserver1']
            , config['nameserver2']
            )

    with open('/etc/sysconfig/network-scripts/ifcfg-enp3s0', 'w') as f:
        f.write(output)


    os.system("systemctl restart network")

def listen_for_message():
    # https://pypi.org/project/redis/ (MIT License!)
    p =  r.pubsub() # Get a pubsub object, python redis library
    p.subscribe("CONFIGURATION_CHANGED")
    while True:
        message = p.get_message()
        if message:
            write_to_disk()
        time.sleep(1)  # No need to check ALL the time, snore.

if __name__ == "__main__":
    # write_to_disk()
    listen_for_message()

