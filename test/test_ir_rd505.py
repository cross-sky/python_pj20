'''
Author: your name
Date: 2021-12-23 13:59:32
LastEditTime: 2021-12-25 17:37:39
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\test\test_ir_rd505.py
'''
from rd505_ir import *

import pytest

def print_ir(func, data,dicts):
    func(data)
    print(dicts)

def test_str_to_hex():
    #data1 = '40 00 14 81 26 82 2C C0 00 00 04 3A 02 81 49 5F'
    data1 = '40 00 14 81 26 4E 34 C0 00 00 00 37 02 97 4F 66'
    process = Rd505IrProcess()
    process.decode_ir(data1)
    print("{")
    for k, v in process.irdict.items():
        print(f"{k!r}: {v!r}")
    print("}")

    data2 = '40 00 14 81 3F 07 00 01 40 0F 37'
    print_ir(process.decode_ir, data2, process.irdict)
    #pprint.pprint(process.irdict)

    data3 = '40 00 14 81 3F 08 00 01 40 0F 38'
    print_ir(process.decode_ir, data3, process.irdict)

    data3 = '40 00 14 81 3F 08 00 00 40 0F 37'
    print_ir(process.decode_ir, data3, process.irdict)
