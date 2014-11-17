#!/usr/bin/env python
# -*- coding: utf-8 -*-

# unit tests for nhelper.py
import unittest
from nhelper import *

class TestNetworkTools(unittest.TestCase):
    def test_convert_mask_with_slash(self):
        self.assertEqual(convert_mask('/4'), '240.0.0.0')
        self.assertEqual(convert_mask('/4', 'decimal'), '240.0.0.0')
        self.assertEqual(convert_mask('/4', 'binary'),
                         '11110000.00000000.00000000.00000000')
        self.assertEqual(convert_mask('/4', 'slash'), '/4')
        self.assertEqual(convert_mask('/30'), '255.255.255.252')
        self.assertEqual(convert_mask('/30', 'binary'),
                         '11111111.11111111.11111111.11111100')

    def test_convert_mask_with_decimal(self):
        self.assertEqual(convert_mask('240.0.0.0'), '/4')
        self.assertEqual(convert_mask('240.0.0.0', 'decimal'), '240.0.0.0')
        self.assertEqual(convert_mask('240.0.0.0', 'binary'),
                         '11110000.00000000.00000000.00000000')
        self.assertEqual(convert_mask('240.0.0.0', 'slash'), '/4')
        self.assertEqual(convert_mask('255.255.255.252', 'binary'),
                         '11111111.11111111.11111111.11111100')
        self.assertEqual(convert_mask('255.255.255.252', 'slash'), '/30')

    def test_convert_mask_with_binary(self):
        self.assertEqual(convert_mask('11110000.00000000.00000000.00000000'),
                         '240.0.0.0')
        self.assertEqual(convert_mask('11110000.00000000.00000000.00000000',
                                      'decimal'), '240.0.0.0')
        self.assertEqual(convert_mask('11110000.00000000.00000000.00000000',
                                      'binary'),
                         '11110000.00000000.00000000.00000000')
        self.assertEqual(convert_mask('11110000.00000000.00000000.00000000',
                                      'slash'), '/4')
        self.assertEqual(convert_mask('11111111.11111111.11111111.11111100',
                                      'decimal'), '255.255.255.252')
        self.assertEqual(convert_mask('11111111.11111111.11111111.11111100',
                                      'slash'), '/30')

    def test_load_ip_address_description(self):
        self.assertEqual(ipv4[0].get('224.0.0.19'), \
                        'IS-IS over IP')
        self.assertEqual(ipv4[1].get('203.0.113.0/24'), \
                        'TEST-NET-3')

    def test_IPAddress_class_wrong_ip(self):
        self.assertRaises(IPAddress.WrongIPError,
                          IPAddress, '300.300.300.300/24')
        self.assertRaises(IPAddress.WrongIPError,
                          IPAddress, '400')
        self.assertRaises(IPAddress.WrongIPError,
                          IPAddress, '1.2.3.4/32', version='ip')

    def test_IPAddress_class_ipv4_one(self):
        test_ip = IPAddress('192.168.1.3/30')
        self.assertEqual(test_ip.ip, '192.168.1.3')
        self.assertEqual(test_ip.mask, '255.255.255.252')
        self.assertEqual(test_ip.get_class(), 'C')
        self.assertTrue(test_ip.is_in_range(IPAddress('192.168.0.0'),
                                            IPAddress('193.0.0.0')))
        self.assertTrue(test_ip.is_in_range(IPAddress('192.168.0.0'),
                                            IPAddress('192.168.1.3')))
        self.assertFalse(test_ip.is_in_range(IPAddress('224.0.0.0'),
                                            IPAddress('224.255.255.255')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('192.168.1.0/24')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('192.168.0.0 255.255.254.0')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('192.168.1.0')))
        self.assertFalse(test_ip.is_in_subnet(Subnet('10.0.0.0/8')))
        self.assertFalse(test_ip.is_subnet())
        self.assertEqual(test_ip.get_network(), Subnet('192.168.1.0/30'))
        self.assertEqual(test_ip.get_description(), 'Private-Use Networks')
        self.assertEqual(test_ip.get_summary(), '%s\n%s\n%s\n%s' \
                          % ('192.168.1.3', '255.255.255.252',
                             'Class C', 'Private-Use Networks'))

    def test_IPAddress_class_ipv4_two(self):
        test_ip = IPAddress('224.0.0.9')
        self.assertEqual(test_ip.ip, '224.0.0.9')
        self.assertEqual(test_ip.get_class(), 'D')
        self.assertTrue(test_ip.is_in_range(IPAddress('224.0.0.9'),
                                            IPAddress('224.0.0.10')))
        self.assertTrue(test_ip.is_in_range(IPAddress('224.0.0.0'),
                                            IPAddress('239.255.255.255')))
        self.assertFalse(test_ip.is_in_range(IPAddress('10.0.0.0'),
                                            IPAddress('10.255.255.255')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('224.0.0.0/24')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('0.0.0.0 0.0.0.0')))
        self.assertFalse(test_ip.is_in_subnet(Subnet('192.168.0.0 255.255.0.0')))
        self.assertFalse(test_ip.is_in_subnet(Subnet('10.0.0.0/8')))
        self.assertFalse(test_ip.is_subnet())
        self.assertEqual(test_ip.get_network(), None)
        description = ('The Routing Information Protocol (RIP) version 2'
                       ' group address is used to send routing information '
                       'to all RIP2-aware routers on a network segment.')
        self.assertEqual(test_ip.get_description(), description)
        self.assertEqual(test_ip.get_summary(), '%s\n%s\n%s' \
                          % ('224.0.0.9',
                             'Multicast', description))

    def test_IPAddress_class_ipv4_three(self):
        test_ip = IPAddress('10.10.20.0')
        self.assertEqual(test_ip.ip, '10.10.20.0')
        self.assertEqual(test_ip.get_class(), 'A')
        self.assertTrue(test_ip.is_in_range(IPAddress('10.0.0.0'),
                                            IPAddress('11.0.0.0')))
        self.assertTrue(test_ip.is_in_range(IPAddress('10.10.20.0'),
                                            IPAddress('10.10.20.255')))
        self.assertFalse(test_ip.is_in_range(IPAddress('13.10.3.4'),
                                            IPAddress('14.20.31.1')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('10.0.0.0')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('0.0.0.0 0.0.0.0')))
        self.assertFalse(test_ip.is_in_subnet(Subnet('192.168.0.0 255.255.0.0')))
        self.assertTrue(test_ip.is_in_subnet(Subnet('0.0.0.0/4')))
        self.assertFalse(test_ip.is_in_subnet(Subnet('170.162.2.0/24')))
        self.assertFalse(test_ip.is_subnet())
        self.assertEqual(test_ip.get_network(), Subnet('10.0.0.0'))

        self.assertEqual(test_ip.get_description(), 'Private-Use Networks')
        self.assertEqual(test_ip.get_summary(), '%s\n%s\n%s\n%s' \
                          % ('10.10.20.0', '255.0.0.0',
                             'Class A', 'Private-Use Networks'))

    def test_Subnet_class_wrong_network_address(self):
        self.assertRaises(Subnet.WrongSubnetError,
                          Subnet, '10.10.10.1/24')
        self.assertRaises(Subnet.WrongSubnetError,
                          Subnet, '192.168.1.0/23')

    # TODO: add more tests

if __name__ == '__main__':
    load_ip_address_description()
    #unittest.main()
    a = Subnet('192.168.1.0/27')
    print('{ip} {mask}'.format(ip=a.ip, mask=a.get_mask()))
    print(a.get_first_address())
    print(a.get_broadcast_address())
    print(a.get_last_address())
    print(a.get_mask())
    print(a.get_wildcard())

    # r1 = Router("R1")
    # sw1 = Switch("SW1")
    # fa = Interface('fa0/1', IPAddress('192.168.10.5/30'))
    # r1.add_interface(fa)
    # fa = Interface('fa0/2', IPAddress('192.168.1.5/30'))
    # r1.add_interface(fa)
    # print(r1.build_config())
    # print('----------------------------')
    # fa = Interface('fa0/2', vlan="10")
    # sw1.add_interface(fa)
    # fa = Interface('fa0/3', vlan="trunk")
    # sw1.add_interface(fa)
    # print(sw1.build_config())