'''
Author: your name
Date: 2022-04-09 10:04:10
LastEditTime: 2022-04-14 22:03:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\test\test_rd505_cmd.py
'''

import pytest
import sys
import time
#import logging
from rd505_cmd import *

#logging.basicConfig(level=logging.DEBUG)
sys.path.append("..")

def myprint(dat_dict):
    # print('RCCONTROL_ADDR: {}'.format(hex(dat_dict['RCCONTROL_ADDR'])))
    logging.debug('RCCONTROL_ADDR: {}'.format(hex(dat_dict['RCCONTROL_ADDR'])))
    logging.debug('MAIN_ADDR: {}'.format(hex(dat_dict['MAIN_ADDR'])))
    logging.debug('DATA_LEN: {}'.format(hex(dat_dict['DATA_LEN'])))
    logging.debug('DATA_CMD: {}'.format(hex(dat_dict['DATA_CMD'])))
    logging.debug('CMD_REPLAY: {}'.format(hex(dat_dict['CMD_REPLAY'])))
    logging.debug('SYSTEM_MODE: {}'.format(SYSTEM_MODE_DICT.get(dat_dict[SYSTEM_MODE])))
    logging.debug('CMD_TYPE: {}'.format(CMD4C_TYPE_DIC.get(dat_dict[CMD_TYPE])))
    logging.debug('WIND_SPEED: {}'.format(WIND_SPEED_DIC.get(dat_dict[WIND_SPEED])))
    logging.debug('WIN_DIR_UP: {}'.format(WIN_DIR_UP_DIC.get(dat_dict[WIN_DIR_UP])))
    logging.debug('SYS_TEMPT: {}'.format(dat_dict[SYS_TEMPT]))
    logging.debug('WIN_DIR_LR: {}'.format(WIN_DIR_LR_DIC.get(dat_dict[WIN_DIR_LR])))
    
def myprint_cmd49Res(dat_dict):
    logging.debug('ERROR_SYSTEM_NUM: {}'.format(hex(dat_dict[ERROR_SYSTEM_NUM])))
    logging.debug('ERROR_INDOOR_NUM: {}'.format(hex(dat_dict[ERROR_INDOOR_NUM])))
    logging.debug('ERROR_CODE: {}'.format(hex(dat_dict[ERROR_CODE])))



    
def test_decode_cmd4c_temp():
    data = '40 00 11 06 08 4C 09 75 6E 09 08 '
    dec_cmd4c = RD505CMD(data)
    dec_cmd4c.cmd_check()

    myprint(dec_cmd4c.data_decode_dict)

def test_decode_cmd4c_wind_up():
    data = '40 00 11 06 08 4C 11 1C 7A 1B 7F'
    dec_cmd4c = RD505CMD(data)
    dec_cmd4c.cmd_check()

    myprint(dec_cmd4c.data_decode_dict)   

def test_decode_cmd4c_wind_lr():
    data1 = '40 00 11 05 08 4C 0A 55 6C 23  '
    data2 = '40 FE 10 05 00 4C E2 55 6C 3C   '
    data3 = '40 FE 10 05 00 4C E2 13 6C 7A '
    data4 = '40 00 11 05 08 4C 12 13 6C 7D  '

    datas = [data1, data2, data3, data4] #
    for i in range(len(datas)):
        dec_cmd4c = RD505CMD(datas[i])
        dec_cmd4c.cmd_check()
        myprint(dec_cmd4c.data_decode_dict)
        logging.debug('----------------------------')

def test_decode_cmd49_resmain():
    data1 = '00 FE 58 06 80 49 08 00 00 40 21'
    data2 = '00 FE 58 06 80 49 08 00 00 41 20'
    data3 = '00 FE 58 06 80 49 08 00 49 41 69'
    data4 = ' 00 FE 58 06 80 49 08 00 EC 40 CD'
    data5 = '00 FE 58 06 80 49 08 00 49 40 68'

    datas = [data1, data2, data3, data4, data5] #, data3, data4
    for i in range(len(datas)):
        dec_cmd49 = RD505CMD(datas[i])
        dec_cmd49.cmd_check()
        myprint_cmd49Res(dec_cmd49.data_decode_rescmd49)
        logging.debug('----------------------------')


def test_fcc_check():
    data = '00 FE 58 06 80 49 08 00 00 40 21'
    assert(checkFcc(data) != '')


