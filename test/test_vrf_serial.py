'''
Author: your name
Date: 2021-11-18 11:05:43
LastEditTime: 2021-11-18 14:27:04
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\test\vrf_serial.py
'''
from myserial.vrf_serial import *

import pytest


def test_str_to_hex():
    '''
    hexstr = '001122334455' -> [0x00, 0x 11]  bytes.fromhex(hexstr)
    str = '\x1c\x53'  ->  [x1c,0x53]   ord(c) or c in x             
    lists=[x1c,0x53]-> '\x53,\x21\x6a'   str(bytearry(x))
    [x1c,0x53]-> '1c53'   
    '''
    s = '00 11 22 33 44'
    r_bytes = hexstringToBytes(s)
    print(type(r_bytes))
    hex_list = bytesToHexstring(r_bytes)
    print(hex_list)
    #print(str(r_bytes))


def test_bytes_to_str():
    bs = b'\x00\x11\x22\x33'
    str_data = bytesToHexstring(bs)
    print(str_data)

def test_printf():
    f_name = r'myserial/'+'a.txt'
    f_file = open(f_name, 'w')
    print(time.strftime("%Y-%m-%d %X: ") + 'bbbb', file=f_file, flush=False)
    f_file.close()