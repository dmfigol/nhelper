#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this module contains some basic helper functions
# like network division, netmask recalculation
import re
import random
import json
import os
import string
import shutil

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
              'Serial', 'Vlan', 'Tunnel', 'Portchannel']
TEMPLATES_DIR = "templates"

def generate_random_password(length=20):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                   for _ in range(length))

def autocomplete_interface(full_name):
    match = re.search('^([a-zA-Z]+)([0-9\/].*)$', full_name)
    for interface in INTERFACES:
        if interface.lower().startswith(match.group(1).lower()):
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
    def __init__(self, name):
        self.name = name
        self.interfaces = []
        self.type = None
        self.domain_name = "cisco.com"
        self.vendor = "cisco"
        self.users = {}
        self.eigrp = False
        self.ospf = False
        self.static_routes = []
        self.eigrp_as = None
        self.ospf_process = None
        self.ipv4_routing = False
        self.syslog_server = ""
        self.ntp_server = ""
        self.ipsec_tunnels = []
        self.next_acl_number = 150
        self.json = {}

    def __str__(self):
        return self.name

    def get_interface(self, name):
        for interface in self.interfaces:
            if interface.name == autocomplete_interface(name):
                return interface

    def set_domain_name(self, domain):
        if domain:
            self.domain_name = domain

    def set_ntp_server(self, server):
        if server:
            self.ntp_server = server

    def set_syslog_server(self, server):
        if server:
            self.syslog_server = server

    def parse_options_json(self, options):
        self.domain_name = options.get("domain_name")
        self.ntp_server = options.get("ntp_server")
        self.syslog_server = options.get("syslog_server")
        self.parse_users_json(options.get("users", []))

    def parse_users_json(self, users):
        self.users = {}
        for user in users:
            password = user.get('password')
            if not password:
                password = generate_random_password()
            self.users[user['username']] = password

    def generate_json(self):
        self.json["name"] = self.name
        self.json["type"] = self.type
        self.json["ipv4_routing"] = self.ipv4_routing
        self.json["ospf"] = self.ospf
        self.json["ospf_process"] = self.ospf_process
        self.json["eigrp"] = self.eigrp
        self.json["eigrp_as"] = self.eigrp_as
        interfaces_json = []
        for interface in self.interfaces:
            interfaces_json.append(interface.generate_json())
        self.json["interfaces"] = interfaces_json
        if self.static_routes:
            self.json["static_routes"] = self.static_routes
        return self.json


    # def check_routing(self):
    #     self.eigrp = [interface for interface in self.interfaces
    #                   if interface.routing == 'eigrp']
    #     self.ospf = [interface for interface in self.interfaces
    #                   if interface.routing == 'ospf']

    def generate_routing_config(self):
        result = []
        if self.ipv4_routing and self.eigrp:
            result.append("router eigrp {}".format(self.eigrp_as))
            for interface in self.interfaces:
                if interface.eigrp:
                    result.append(" network {} 0.0.0.0".format(interface.ip_address))
            result.append(" passive-interface default")
            for interface in self.interfaces:
                if interface.eigrp and interface.eigrp_not_passive:
                    result.append(" no passive-interface {}".format(interface.name))
            result.append("!")
        if self.ipv4_routing and self.ospf:
            result.append("router ospf {}".format(self.ospf_process))
            for interface in self.interfaces:
                if interface.ospf:
                    result.append(" network {} 0.0.0.0 area {}".format(interface.ip_address,
                                                                       interface.ospf_area))
            result.append(" passive-interface default")
            for interface in self.interfaces:
                if interface.ospf and interface.ospf_not_passive:
                    result.append(" no passive-interface {}".format(interface.name))
            result.append("!")
        result.append('\n')
        return '\n'.join(result)

    def generate_ssh_config(self):
        if self.vendor == 'cisco':
            snippet_path = os.path.join(TEMPLATES_DIR, 'cisco/ssh.cfg')
        with open(snippet_path) as f:
            snippet = f.read()
            return snippet.format(domain=self.domain_name)

    def generate_static_routing_config(self):
        config = []
        for static_route in self.static_routes:
            prefix = IPAddress(static_route.get("prefix"))
            nexthop = static_route.get("nexthop")
            config.append("ip route {} {} {}\n".format(prefix.ip,
                                                      prefix.get_mask(),
                                                      nexthop))
        return ''.join(config)

    def build_config(self):
        config = []
        config.append("hostname {name}\n".format(name = self.name))
        for tunnel in self.ipsec_tunnels:
            config.append(tunnel.build_configuration(self))
        config.append(self.build_config_interfaces())
        config.append(self.generate_routing_config())
        config.append(self.generate_static_routing_config())
        config.append(self.build_config_users())
        if self.ntp_server:
            if self.vendor == 'cisco':
                config.append("ntp server {}\n".format(self.ntp_server))
        if self.syslog_server:
            if self.vendor == 'cisco':
                config.append("logging {}\n".format(self.syslog_server))
        config.append(self.generate_ssh_config())
        return ''.join(config)

    def add_interface(self, interface):
        if interface in self.interfaces:
            print("%s already exists" % interface)
        else:
            self.interfaces.append(interface)
            if self.type == "switch":
                if interface.type == "access":
                    self.add_vlan_from_interface(interface)
                elif 'Vlan' in interface.name:
                    vlan_num = int(re.match("Vlan ?(\d+)", interface.name).group(1))
                    self.vlans.add(vlan_num)

    def build_config_interfaces(self, native_vlan=0, vlan_list=None):
        if vlan_list is None:
            vlan_list = []
        vlan_list = sorted([str(vlan) for vlan in vlan_list])
        result = [interface.build_config(native_vlan, vlan_list)
                  for interface in self.interfaces]
        return '\n'.join(result) + '\n'

    def build_config_users(self):
        if self.vendor == 'cisco':
            snippet_path = os.path.join(TEMPLATES_DIR, 'cisco/users.cfg')
        with open(snippet_path) as f:
            snippet = f.read()
            result = []
            for user, password in self.users.items():
                result.append(snippet.format(user=user, password=password))
            result.append('')
            return '\n'.join(result)


class Router(NetworkDevice):
    def __init__(self, name):
        super(Router, self).__init__(name)
        self.type = "router"
        self.ipv4_routing = True


class Switch(NetworkDevice):
    def __init__(self, name):
        super(Switch, self).__init__(name)
        self.type = "switch"
        self.vlans = set()
        self.routing = False
        self.ipv4_routing = False
        self.l3_int_number = 0
        self.vtp_mode = "transparent"
        self.stp_mode = "rapid-pvst"

    def add_vlan_from_interface(self, interface):
        self.vlans.add(interface.vlan)

    def set_vtp_mode(self, mode):
        self.vtp_mode = mode

    def set_stp_mode(self, mode):
        self.stp_mode = mode

    # def add_additional_settings(self):
    #     self.set_vtp_mode("transparent")
    #     self.set_stp_mode("rapid-pvst")

    def add_to_switch_group(self, switch_group):
        switch_group.append(self)
        for interface in self.interfaces:
            if interface.other_end:
                if interface.other_end.device.type == 'switch':
                    neighbor_switch = interface.other_end.device
                    if neighbor_switch not in switch_group:
                        neighbor_switch.add_to_switch_group(switch_group)
                elif interface.other_end.device.type == 'router':
                    for subif in interface.other_end.children:
                        self.vlans.add(subif.dot1q)


    def build_config(self):
        #self.check_routing()
        #self.add_additional_settings()
        config = []
        config.append("hostname {}\n".format(self.name))
        if self.stp_mode:
            config.append("spanning-tree mode {}\n".format(self.stp_mode))
        if self.vtp_mode:
            config.append("vtp mode {}\n".format(self.vtp_mode))
        config.append(self.build_vlan_config())
        config.append(self.build_config_interfaces(self.native_vlan, self.vlans))
        if self.ipv4_routing:
            config.append("ip routing\n")
        config.append(self.generate_routing_config())
        config.append(self.generate_static_routing_config())
        config.append(self.build_config_users())
        if self.ntp_server:
            config.append("ntp server {}\n".format(self.ntp_server))
        if self.syslog_server:
            config.append("logging {}\n".format(self.syslog_server))
        config.append(self.generate_ssh_config())
        return ''.join(config)

    def build_vlan_config(self):
        config = []
        for vlan in sorted(self.vlans):
            config.append("vlan {vlan_number}".format(vlan_number = vlan))
            if vlan == self.native_vlan:
                config.append(" name Native")
            config.append("!")
        config.append('')
        return '\n'.join(config)


class Interface(object):
    def __init__(self, name, ip_address=None, vlan=None, routing=None, device=None):
        self.name = autocomplete_interface(name)
        self.up = True
        self.type = None
        self.ip_address = None
        self.ospf = False
        self.ospf_area = None
        self.ospf_not_passive = False
        self.eigrp = False
        self.eigrp_not_passive = False
        self.routing = routing
        self.device = device
        self.crypto_map = None
        self.switchport = False
        self.dot1q = None
        self.other_end = None
        self.line = None
        self.json = {}
        self.parent = None
        self.children = []
        self.vlan = None
        if ip_address:
            if self.device.type == 'switch':
                self.device.l3_int_number += 1
            self.ip_address = IPAddress(ip_address)
        if vlan:
            if vlan == "trunk":
                self.type = "trunk"
            else:
                self.type = "access"
                self.vlan = int(vlan)

    def generate_json(self):
        self.json["name"] = self.name
        self.json["up"] = self.up
        self.json["switchport"] = self.switchport
        if self.ip_address:
            self.json["ip"] = "{}{}".format(self.ip_address.ip,
                                            convert_mask(self.ip_address.get_mask(), 'slash'))
        else:
            self.json["ip"] = None
        self.json["ospf_enabled"] = self.ospf
        self.json["ospf_area"] = self.ospf_area
        self.json["ospf_not_passive"] = self.ospf_not_passive
        self.json["eigrp_enabled"] = self.eigrp
        self.json["eigrp_not_passive"] = self.eigrp_not_passive

        if self.type == "trunk":
            self.json["vlan"] = "trunk"
        elif self.type == "access":
            self.json["vlan"] = self.vlan
        self.json["dot1q"] = self.dot1q

        return self.json

    def build_config(self, native_vlan=None, vlan_list=[]):
        config = ["interface {}".format(self.name)]
        if self.dot1q:
            config.append(" encapsulation dot1q {}".format(self.dot1q))
        if self.switchport:
            if self.type == "trunk":
                config.append(" switchport trunk encapsulation dot1q")
                config.append(" switchport mode trunk")
                config.append(" switchport trunk allowed vlan {}"
                              .format(','.join(vlan_list)))
                if native_vlan:
                    config.append(" switchport trunk native vlan {vlan}"
                                  .format(vlan = native_vlan))
                config.append(" switchport nonegotiate")
            elif self.type == "access":
                config.append(" switchport mode access")
                config.append(" switchport access vlan {}"
                              .format(self.vlan))
                config.append(" spanning-tree portfast")
                config.append(" spanning-tree portfast bpduguard ")
        elif self.ip_address:
            if self.device.type == 'switch' and 'Ethernet' in self.name:
                config.append(" no switchport")
            config.append(" ip address {} {}".format(self.ip_address.ip,
                                                     self.ip_address.get_mask()))
            if self.crypto_map:
                config.append(" crypto map {}".format(self.crypto_map))
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

class Tunnel(object):
    def __init__(self, json, endpoints):
        self.json = json
        self.endpoints = endpoints
        self.key = generate_random_password()
        self.details = {}
        self.find_missing_parts()

    def other(self, router):
        for endpoint in self.endpoints:
            if endpoint is not router:
                return endpoint

    def find_missing_parts(self):
        for router in self.endpoints:
            details = {}
            router.ipsec_tunnels.append(self)
            other_router = self.other(router)
            tunnel_src_int = router.get_interface(self.json[router.name]["tunnel_int"])
            tunnel_src_int.crypto_map = "CMAP"
            details["tunnel_src_int"] = tunnel_src_int
            details["tunnel_dst_int"] = other_router.get_interface(self.json[other_router.name]["tunnel_int"])
            details["src_traffic"] = Subnet(self.json[router.name]["encrypted_traffic"])
            details["dst_traffic"] = Subnet(self.json[other_router.name]["encrypted_traffic"])
            details["acl_number"] = router.next_acl_number
            router.next_acl_number += 1
            self.details[router.name] = details

    def build_configuration(self, router):
        if router.vendor == 'cisco':
            snippet_path = os.path.join(TEMPLATES_DIR, 'cisco/ipsec_vpn.cfg')
        with open(snippet_path) as f:
            snippet = f.read()
            return snippet.format(tunnel_key = self.key,
                                  acl_num = self.details[router.name]["acl_number"],
                                  tunnel_end_ip = self.details[router.name]["tunnel_dst_int"].ip_address,
                                  src_ip = self.details[router.name]["src_traffic"].ip,
                                  src_ip_wc = self.details[router.name]["src_traffic"].get_wildcard(),
                                  dst_ip = self.details[router.name]["dst_traffic"].ip,
                                  dst_ip_wc = self.details[router.name]["dst_traffic"].get_wildcard())

class Topology(object):
    def __init__(self, json_file):
        self.json = get_input_topology(json_file)
        self.nodes = []
        self.broadcast_domains = []
        self.switches = []
        self.links = self.json['topology'].get('links')
        self.index = {}
        self.ipsec_tunnels = []
        users =  self.parse_users(self.json.get("options").get("users", []))
        for node_json in self.json["topology"]["nodes"]:
            if node_json['type'] == 'router':
                node = Router(node_json['name'])
            elif node_json['type'] == 'switch':
                node = Switch(node_json['name'])
                self.switches.append(node)
            node.json = node_json
            for interface_json in node_json['interfaces']:
                interface = Interface(name=interface_json['name'],
                                      ip_address=interface_json.get('ip'),
                                      vlan=interface_json.get('vlan'),
                                      routing=interface_json.get('routing'),
                                      device = node)
                node.add_interface(interface)
            node.users = users
            node.set_domain_name(self.json.get("options").get("domain_name"))
            node.set_ntp_server(self.json.get("options").get("ntp_server"))
            node.set_syslog_server(self.json.get("options").get("syslog_server"))
            self.nodes.append(node)
            self.index[node.name] = node
        self.calculate_topology()
        self.parse_ipsec_tunnels(self.json.get("options").get("ipsec_tunnel", []))
        self.parse_users(self.json.get("options").get("users", []))

    def calculate_topology(self):
        vlans = set()
        vlans.add(1)
        for switch in self.switches:
            vlans |= switch.vlans
        vlan_range = set(range(500, 1001)) - vlans
        native_vlan = random.sample(vlan_range, 1)[0]
        vlans.add(native_vlan)
        for switch in self.switches:
            switch.native_vlan = native_vlan
            switch.vlans = vlans
            if switch.l3_int_number > 1:
                switch.routing = True

    def parse_ipsec_tunnels(self, json):
        for tunnel_json in json:
            endpoints = [self.index[router] for router in tunnel_json.keys()]
            tunnel = Tunnel(tunnel_json, endpoints)
            self.ipsec_tunnels.append(tunnel)

    def parse_users(self, users):
        d = {}
        for user in users:
            password = user.get('password')
            if not password:
                password = generate_random_password()
            d[user['username']] = password
        return d

    def __str__(self):
        return self.json.dumps()

    def create_configs(self):
        directory = "configs"
        shutil.rmtree(directory, ignore_errors=True)
        os.makedirs(directory)
        for node in self.nodes:
            with  open('{path}/{filename}.cfg'
                       .format(path=directory,
                               filename = node.name), 'w') as f:
                f.write(node.build_config())
