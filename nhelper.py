#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module contains some basic helper functions
# like network division, netmask recalculation
import re
import random
import json
import os
import jinja2

ipv4 = [{}, {}]
ipv6 = [{}, {}]

ip_to_class = {'0': 'A', '10': 'B', '110': 'C',
                     '1110': 'D', '1111': 'E'}
class_info = {'A': ['255.0.0.0', 'Class A'],
              'B': ['255.255.0.0', 'Class B'],
              'C': ['255.255.255.0', 'Class C'],
              'D': ['', 'Multicast'],
              'E': ['', 'Experimental'],}

IPV4_RE = re.compile(r'((\d+\.){3}\d+)(\/\d+| +(\d+\.){3}\d+| *- *(\d+\.){3}\d+)?')

INTERFACES = ['FastEthernet', 'GigabitEthernet', 'Ethernet', 'Loopback',
              'Serial', 'Vlan']

def autocomplete_interface(full_name):
    match = re.search('^([a-zA-Z]+)([0-9/].*)$', full_name)
    for interface in INTERFACES:
        if interface.lower().startswith(match.group(1)):
            return '{interface}{number}'.format(interface = interface,
                                                number = match.group(2))

def load_ip_address_description():
    def helper(filename, hashmap):
        for line in filename:
            array = line.split('\t')
            if re.match('((\d+\.){3}\d+)', array[0].strip()):
                if '/' in array[0] or '-' in array[0] \
                    or array[0].count('.') > 3:
                    hashmap[1][array[0].strip()] = array[1].strip()
                else:
                    hashmap[0][array[0].strip()] = array[1].strip()
            else:
                pass

    with open('ipv4.txt', 'r') as f4, open('ipv6.txt', 'r') as f6:
        helper(f4, ipv4)
        helper(f6, ipv6)

def convert_mask(netmask, view=None):
    """Converts netmask to the desired form specified by the
    view paramater. If view is not specified, then the mask will be
    converted into slash notation if it was previously specified 
    in decimal form, or into decimal form otherwise.
    Input:
      netmask - string, mask needed to be converted
      view - string, desired notation. Can be one of three:
            'decimal', 'slash' or 'binary'
    Output:
       string, netmask in the desired form
    """
    netmask = netmask.strip()
    if '/' in netmask:
        if view == 'slash':
            return netmask
        number_of_unities = int(netmask[1:])
        bin_form = ['1' for n in range(number_of_unities)] + \
                    ['0' for n in range(32 - number_of_unities)]
        # insert '.' to show octets
        for i in range(1, 4):
            bin_form.insert(32 - 8 * i, '.')
        bin_form = ''.join(bin_form)
        return convert_mask(bin_form, view)

    elif re.match('(([01]){8}\.){3}([01]){8}$', netmask):
        if view == 'binary':
            return netmask
        elif view == 'slash':
            count = 0
            for symbol in netmask:
                if symbol == '1':
                    count += 1
                elif symbol == '0':
                    break
            return '/%d' % count
        elif not view or view == 'decimal':
            octets = [str(int(octet, 2)) for octet in netmask.split('.')]
            return '.'.join(octets)

    elif re.match('^[01]{32}$', netmask):
        netmask = list(netmask)
        for i in range(1, 4):
            netmask.insert(32 - 8 * i, '.')
        netmask = ''.join(netmask)
        if view == 'binary':
            return netmask
        elif view == 'slash':
            count = 0
            for symbol in netmask:
                if symbol == '1':
                    count += 1
                elif symbol == '0':
                    break
            return '/%d' % count
        elif not view or view == 'decimal':
            octets = [str(int(octet, 2)) for octet in netmask.split('.')]
            return '.'.join(octets)


    elif re.match('(\d+\.){3}\d+$', netmask):
        if view == 'decimal':
            return netmask
        octets = ['{0:08b}'.format(int(octet)) \
                  for octet in netmask.split('.')]
        bin_form = '.'.join(octets)
        if view == 'binary':
            return bin_form
        elif not view or view == 'slash':
            return convert_mask(bin_form, 'slash')
    else:
        print('wrong input')

def summarize_subnets(subnets, view='decimal', smart=False):
    pass

def convert_to_wildcard(ip, view='decimal'):
    """Returns inverted ip address in the given notation.
    Input:
      ip - ip address in binary form
      view - string, desired notation. Can be one of three:
            'decimal', 'slash' or 'binary'
    Output:
      string - ip address in the given notation
    """
    ip = int(ip.replace('.', ''), 2)
    all_ones_mask = int(convert_mask("255.255.255.255", 'binary')
                    .replace('.', ''), 2)
    wildcard = bin(ip ^ all_ones_mask)[2:].zfill(32)
    return convert_mask(wildcard, view)

def get_input_topology(path):
    with open(path) as f:
        topology = json.load(f)
    return topology

class IPAddress(object):
    """Ip address model with a lot of helper functions,
    like: converting ip to the binary form,
    showing additional description if exists,
    if ip address belongs to the network
    what network is associated with current ip address and mask
    and so on
    * TODO: ipv6 
    """
    class WrongIPError(Exception):
        """Raise if input ip notation is wrong
        """
        pass


    def __init__(self, ip_address, version='ipv4'):
        """Initializes instance of IPAddress class.
        Input:
          ip_address - string, for ipv4 one of three options:
            1.2.3.4
            1.2.3.4/24
            1.2.3.4 255.255.255.0
          version - string, one of two options:
            ipv4
            ipv6 - not implemented yet
        Output: None
        """
        self.version = version
        if version == 'ipv4':
            match = re.match(IPV4_RE, ip_address.strip())
            if match:
                self.ip = match.group(1)
                self.ip_binary = self.get_binary_form()
                if len(self.ip_binary) != 32:
                    raise IPAddress.WrongIPError('This is not a '
                                                 'valid ipv4 address')
                # if netmask is specified
                if match.group(3):
                    self.mask = convert_mask(match.group(3), 'decimal')
            else:
                raise IPAddress.WrongIPError('This is not a '
                                             'valid ipv4 address')
        elif version == 'ipv6':
            # TODO
            pass
        else:
            raise IPAddress.WrongIPError('This is not a valid ip address')

    def get_binary_form(self):
        """Shows ip address in the binary form without dots.
        Input: None
        Output:
          string, 32-bit ip address in the binary form without dots
        """
        # careful, nevertheless ip address is not a mask
        # function convert_mask is used
        return convert_mask(self.ip, 'binary').replace('.', '')

    def get_class(self):
        """Defines ip address class if classful addressing is used,
        data is taken from the dictionary ip_to_class
        Input: None
        Output:
          string, class of ip address, one of ['A', 'B', 'C', 'D', 'E']
        """
        for key in ip_to_class:
            if self.ip_binary.startswith(key):
                return ip_to_class[key]

    def get_mask(self):
        """Returns a subnet mask for the given ip address. If ip address was
        previously specified with mask, then it is returned,
        classful mask - otherwise.
        Input: None
        Output: string, netmask for the given ip.
        """
        if self.version == 'ipv4':
            try:
                return self.mask
            except AttributeError:
                return class_info[self.get_class()][0]
        elif self.version == 'ipv6':
            pass

    def get_wildcard(self, view='decimal'):
        """Returns a wildcard for the mask of given ip address in the
        given view.
        If the ip address does not have mask, returns '0.0.0.0'
        Input:
          view - string, desired notation. Can be one of three:
          'decimal', 'slash' or 'binary' 
        """
        if not self.mask:
            return convert_mask('0.0.0.0', view)
        return convert_to_wildcard(self.mask_binary, view)

    def is_in_subnet(self, subnet):
        """Shows if ip belongs to the given subnet
        Input: subnet, Subnet class instance
        Output: boolean
        """
        # host is in subnet if host address AND subnet mask = network address
        return int(self.ip_binary, 2) & int(subnet.mask_binary, 2) == \
                                        int(subnet.ip_binary, 2)

    def is_subnet(self):
        """Shows if ip with mask is subnet address
        Input: none
        Output: boolean
        """
        # ip address is subnet if ip address AND mask = this ip address
        mask = self.get_mask()
        if mask:
            mask_binary = convert_mask(mask, 'binary').replace('.', '')
            return int(self.ip_binary, 2) & int(mask_binary, 2) == \
                                        int(self.ip_binary, 2)
        
    def is_in_range(self, low, high):
        """Shows if ip belongs to the given ip address range (inclusive)
        Input:
          low, IPAddress class instance, low boundary
          high, IPAddress class instance, high boundary
        Output: boolean
        """
        ips = []
        for ip in low, self, high:
            ips.append(int(ip.ip_binary, 2))
        # trick: if current ip is in specified range
        # then this array is already sorted
        return ips == sorted(ips)

    def get_description(self):
        """Shows additional description if specified in files ipv4.txt
        or ipv6.txt
        Input: None
        Output: string
        """
        if self.version == 'ipv4':
            description = ipv4[0].get(self.ip, '')
            if not description:
                for key in ipv4[1]:
                    if self.is_in_subnet(Subnet(key)):
                        description = ipv4[1][key]
                        break
        elif self.version == 'ipv6':
            pass
        return description

    def get_summary(self):
        """Shows summary about the ip address, it's decimal representation,
        mask, class, description if exists.
        Input: None
        Output: string, description of the ip address
        """
        summary = []
        summary.append(self.ip)
        mask = self.get_mask()
        if mask:
            summary.append(mask)
        summary.append(class_info[self.get_class()][1])
        description = self.get_description()
        if description:
            summary.append(description)
        return '\n'.join(summary)

    def get_network(self):
        """Shows associated network address if ip address was specified
        with mask, classful network address otherwise.
        Input: None
        Output: Subnet class instance
        """
        mask = self.get_mask()
        if mask:
            mask_binary = convert_mask(mask, 'binary').replace('.', '')
            network_binary = list(bin(int(self.ip_binary, 2) \
                                  & int(mask_binary, 2))[2:].zfill(32))
            for i in range(1, 4):
                network_binary.insert(32 - 8 * i, '.')
            network_address = convert_mask(''.join(network_binary))
            return Subnet('%s %s' % (network_address, mask))
        return None

    def __eq__(self, other):
        """Enable comparison of ip, to count both ip with slash mask
        and decimal form
        Input: other - IPAddress class instance
        Output: Boolean, if two object are equal
        """
        try:
            return self.ip == other.ip, self.get_mask() == other.get_mask()
        except:
            return False

    def __str__(self):
        return self.ip

    def __add__(self, other):
        new_ip = bin(int(self.ip_binary, 2) + other)[2:].zfill(32)
        return IPAddress(convert_mask(new_ip))

    def __sub__(self, other):
        new_ip = bin(int(self.ip_binary, 2) - other)[2:].zfill(32)
        return IPAddress(convert_mask(new_ip))


class Subnet(IPAddress):
    """Model of a subnet with a lot of helper functions,
    like: dividing subnet using VLSM, subnet summarization,
    getting first, last, broadcast ip addresses and many others 
    """

    class WrongSubnetError(Exception):
        """Raise if input ip is not a subnet
        """
        pass

    def __init__(self, ip_address):
        """Initializes Subnet instance based on IPAddress class
        Input:
          ip_address - string, one of three options:
            1.2.3.4
            1.2.3.4/24
            1.2.3.4 255.255.255.0
        Output: None
        """
        super(Subnet, self).__init__(ip_address)        
        if not self.is_subnet():
            raise Subnet.WrongSubnetError("This is not a valid "
                                          "network address")
        self.mask = self.get_mask()
        self.mask_binary = convert_mask(self.mask, 'binary').replace('.', '')

    def get_first_address(self):
        """Returns the first usable host address in the subnet.
        If subnet is /32 returns exact ip address.
        Input: None
        Output: IPAddress object"""
        if (convert_mask(self.get_mask(), view="slash")) == '/32':
            return self
        return self + 1

    def get_broadcast_address(self):
        """Returns the broadcast address of the subnet.
        If subnet is /32 returns exact ip address.
        Input: None
        Output: IPAddress object"""
        if (convert_mask(self.get_mask(), view="slash")) == '/32':
            return self
        network_binary = int(self.ip_binary, 2)
        all_ones_mask = int(convert_mask(self.get_wildcard(), 'binary')
                        .replace('.', ''), 2)
        broadcast_address = bin(network_binary | all_ones_mask)[2:].zfill(32)
        return IPAddress(convert_mask(broadcast_address))

    def get_last_address(self):
        """Returns the last usable host address in the subnet.
        If subnet is /32 returns exact ip address.
        Input: None
        Output: IPAddress object"""
        if (convert_mask(self.get_mask(), view="slash")) == '/32':
            return self
        return self.get_broadcast_address() - 1

class NetworkDevice(object):
    def __init__(self, name, jinja_env):
        self.name = name
        self.interfaces = []
        self.type = None
        self.domain_name = "cisco.com"
        self.vendor = "cisco"
        self.jinja_env = jinja_env


    def __str__(self):
        return self.name

    def set_domain_name(self, domain):
        if domain:
            self.domain_name = domain

    def generate_ssh_config(self):
        template = self.jinja_env.get_template("cisco/ssh.cfg")
        return template.render(domain=self.domain_name)


    def build_config(self):
        config = "hostname {name}\n".format(name = self.name)
        config += self.build_config_interfaces()
        config += self.generate_ssh_config()
        return config

    def add_interface(self, interface):
        if interface in self.interfaces:
            print("%s already exists" % interface)
        else:
            self.interfaces.append(interface)
            if self.type == "switch" and interface.type == "access":
                self.add_vlan_from_interface(interface)

    def build_config_interfaces(self, native_vlan=0):
        result = [interface.build_config(native_vlan)
                  for interface in self.interfaces]
        return '\n'.join(result) + '\n'

class Router(NetworkDevice):
    def __init__(self, name, jinja_env):
        super(Router, self).__init__(name, jinja_env)
        self.type = "router"   

class Switch(NetworkDevice):
    def __init__(self, name, jinja_env):
        super(Switch, self).__init__(name, jinja_env)
        self.type = "switch"
        self.vlans = set()
        self.native_vlan = 0

    def add_vlan_from_interface(self, interface):
        self.vlans.add(interface.vlan)

    def set_vtp_mode(self, mode):
        self.vtp_mode = mode

    def set_stp_mode(self, mode):
        self.stp_mode = mode

    def add_additional_settings(self):
        self.set_vtp_mode("transparent")
        self.set_stp_mode("rapid-pvst")

    def get_random_unused_vlan_number(self):
        vlan_range = set(range(500, 1001)) - self.vlans
        return random.sample(vlan_range, 1)


    def build_config(self):
        self.add_additional_settings()
        config = "hostname {}\n".format(self.name)
        if self.stp_mode:
            config += "spanning-tree mode {}\n".format(self.stp_mode)
        if self.vtp_mode:
            config += "vtp mode {}\n".format(self.vtp_mode)
        config += self.build_vlan_config()
        config += self.build_config_interfaces(self.native_vlan)
        config += self.generate_ssh_config()
        return config

    def build_vlan_config(self):
        self.native_vlan = self.get_random_unused_vlan_number()[0]
        self.vlans.add(self.native_vlan)
        config = []
        for vlan in sorted(self.vlans):
            config.append("vlan {vlan_number}".format(vlan_number = vlan))
            if vlan == self.native_vlan:
                config.append(" name Native")
            config.append("!")
        return '\n'.join(config) + '\n'


class Interface(object):
    def __init__(self, name, ip_address=None, vlan=None):
        self.name = autocomplete_interface(name)
        self.up = True
        self.type = None
        self.ip_address = None
        if ip_address:
            self.ip_address = IPAddress(ip_address)
        if vlan:
            if vlan == "trunk":
                self.type = "trunk"
            else:
                self.type = "access"
                self.vlan = int(vlan)

    def build_config(self, native_vlan):
        config = ["interface {name}".format(name = self.name)]
        if self.ip_address:
            config.append(" ip address {ip} {mask}"
            .format(ip = self.ip_address.ip, mask = self.ip_address.get_mask()))
        if self.type:
            if self.type == "trunk":
                config.append(" switchport trunk encapsulation dot1q")
                config.append(" switchport mode trunk")
                if native_vlan:
                    config.append(" switchport trunk native vlan {vlan}"
                                  .format(vlan = native_vlan))
                config.append(" switchport nonegotiate")
            else:
                config.append(" switchport mode access")
                config.append(" switchport access vlan {vlan}"
                              .format(vlan = self.vlan))
                config.append(" spanning-tree portfast")
                config.append(" spanning-tree portfast bpduguard ")
        if self.up:
            config.append(" no shutdown")
        else:
            config.append(" shutdown")
        config.append("!")
        return '\n'.join(config)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

class Topology(object):

    def __init__(self, json_file, jinja_env):
        self.jinja_env = jinja_env
        self.json = get_input_topology(json_file)
        self.nodes = []
        for node_json in self.json["topology"]["nodes"]:
            if node_json['type'] == 'router':
                node = Router(node_json['name'], jinja_env = self.jinja_env)
            elif node_json['type'] == 'switch':
                node = Switch(node_json['name'], jinja_env = self.jinja_env)
            for interface_json in node_json['interfaces']:
                interface = Interface(name=interface_json['name'],
                                      ip_address=interface_json.get('ip'),
                                      vlan=interface_json.get('vlan'))
                node.add_interface(interface)
            node.set_domain_name(self.json.get("options").get("domain-name"))
            self.nodes.append(node)

    def __str__(self):
        return self.json.dumps()

    def create_configs(self):
        directory = "configs"
        if not os.path.isdir(directory):
            os.makedirs(directory)
        for node in self.nodes:
            with  open('{path}/{filename}.cfg'
                       .format(path=directory,
                               filename = node.name), 'w') as f:
                f.write(node.build_config())