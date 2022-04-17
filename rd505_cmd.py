'''
Author: your name
Date: 2022-04-09 10:03:42
LastEditTime: 2022-04-14 14:34:25
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\rd505_cmd.py
'''

import logging
#from rd505_cmd import *
import sys

logging.basicConfig(level=logging.DEBUG)
sys.path.append("..")


def string_to_bytes(strs):
    '''
    string to bytes
    eg:
    '0123456789ABCDEF0123456789ABCDEF'
    b'0123456789ABCDEF0123456789ABCDEF'
    '''
    return bytes(strs, encoding='utf8')

def string_to_listbytes(strs):
    '''
    string to bytes
    eg:
    '0123456789ABCDEF0123456789ABCDEF'
    b'0123456789ABCDEF0123456789ABCDEF'
    '''
    return bytes.fromhex(strs)
    #return bytes(strs, encoding='utf8')


BIT0 = 1 << 0
BIT1 = 1 << 1
BIT2 = 1 << 2
BIT3 = 1 << 3
BIT4 = 1 << 4
BIT5 = 1 << 5
BIT6 = 1 << 6
BIT7 = 1 << 7

DATA_SA = 0
DATA_DA = 1
DATA_CC = 2
DATA_BC = 3
DATA_EA = 4
DATA_CMD = 5

RCCONTROL_ADDR = 0
MAIN_ADDR = 1
DATA_LEN = 2
DATA_CMD = 3
CMD_REPLAY = 4
SYSTEM_MODE = 5
CMD_TYPE = 6
WIND_SPEED = 7
WIN_DIR_UP = 8
WIN_DIR_LR = 9
SYS_TEMPT = 10

DATA_STATIC_DICT={
    RCCONTROL_ADDR : 'RCCONTROL_ADDR',
    MAIN_ADDR : 'MAIN_ADDR',
    DATA_LEN : 'DATA_LEN',
    DATA_CMD : 'DATA_CMD',
    CMD_REPLAY : 'CMD_REPLAY',
    SYSTEM_MODE : 'SYSTEM_MODE',
    CMD_TYPE : 'CMD_TYPE',
    WIND_SPEED : 'WIND_SPEED',
    WIN_DIR_UP : 'WIN_DIR_UP',
    WIN_DIR_LR : 'WIN_DIR_LR',
    SYS_TEMPT : 'SYS_TEMPT'
}

SYSTEM_MODE_DICT = {
    1 : 'SYSTEM_MODE_WARM',
    2 : 'SYSTEM_MODE_COLD',
    3 : 'SYSTEM_MODE_WIND',
    4 : 'SYSTEM_MODE_WET',
    5 : 'SYSTEM_MODE_AUTO_WARM',
    6 : 'SYSTEM_MODE_AUTO_COLD',
}

CMD4C_TYPE_DIC ={
    BIT3 : 'CMD_TYPE_4C_TEMPE',
    BIT4 : 'CMD_TYPE_4C_WINDSPEED',
    BIT5 : 'CMD_TYPE_4C_UP_WIND_DIR',
    BIT6|BIT7 : 'CMD_TYPE_4C_LR_WIND_DIR',
    BIT6|BIT7|BIT5 :  'CMD_TYPE_4C_UP_LR_WIND_DIR'
}

WIND_SPEED_DIC = {
    2 : 'WIND_SPEED_AUTO',
    3 : 'WIND_SPEED_LEVEL5',
    4 : 'WIND_SPEED_LEVEL3',
    5 : 'WIND_SPEED_LEVEL1',
    BIT6 + 4 : 'WIND_SPEED_LEVEL4',
    BIT6 + 5 : 'WIND_SPEED_LEVEL2',
}

WIN_DIR_UP_DIC = {
    7<<3 : 'WIND_DIR_UD_AUTO_STOP',
    2<<3 : 'WIND_DIR_UD_LEVEL1',
    3<<3 : 'WIND_DIR_UD_LEVEL2',
    4<<3 : 'WIND_DIR_UD_LEVEL3',
    5<<3 : 'WIND_DIR_UD_LEVEL4',
    6<<3 : 'WIND_DIR_UD_LEVEL5',
    1<<3 : 'WIND_DIR_UD_AUTO'
}

WIN_DIR_LR_DIC = {
    7+ (7<<3) : 'WIND_DIR_LR_AUTO_STOP',
    2+ (2<<3) : 'WIND_DIR_LR_LEVEL1',
    3+ (3<<3) : 'WIND_DIR_LR_LEVEL2',
    4+ (7<<3) : 'WIND_DIR_LR_LEVEL3',
    5+ (5<<3) : 'WIND_DIR_LR_LEVEL4',
    6+ (6<<3) : 'WIND_DIR_LR_LEVEL5',
    1+ (1<<3) : 'WIND_DIR_LR_AUTO'
}


DATA_AU0 = 6
DATA_AU1 = 7
DATA_AN = 8
DATA_CA = 9
CMD49RES_DIC = {
    1 : 1
}

CMD_FORMAT_SETTING = 0
CMD_FORMAT_REQUEST = 1
CMD_FORMAT_REPLY = 2
CMD_FORMAT_STATUS_CHANGE = 3

ERROR_SYSTEM_NUM = 0
ERROR_INDOOR_NUM = 1
ERROR_CODE = 2

ERRCODE_DIC = {
    ERROR_SYSTEM_NUM : 'ErrorSystemNum',
    ERROR_INDOOR_NUM : 'ErrorIndoorNum',
    ERROR_CODE : 'ErrorCode'
}

def checkFcc(str_data):
    hex_data = string_to_listbytes(str_data)
    temp = 0
    cc = hex_data[hex_data[DATA_BC]+4]
    d_len = hex_data[DATA_BC]+4
    if d_len > len(hex_data):
        logging.debug('Len error')
        return ''
        
    for i in range(0, hex_data[DATA_BC]+4):
        temp ^= hex_data[i]

    logging.debug('check fcc: {}, data fcc: {}'.format(hex(temp), hex(cc)))
    if((temp&0xff) != cc ):
        logging.debug('FCC CCHECK ERROR!!!')
        return ''
    
    logging.debug('FCC CHECK OK')
    return hex_data


class RD505CMD():
    def __init__(self, data) -> None:
        # self.data_org = data
        self.data = checkFcc(data) #string_to_listbytes(data)
        self.state_dict = {}
    
    # CHECK FCC ERROR
    def cmd_check(self):
        if (self.data != ''):
            self.decodeCmd4cRCcontrol()
            self.decodeCmd49ResMain()

    def decodeCmd4cRCcontrol(self):
        hex_data = self.data
        if (hex_data[DATA_CMD]!= 0x49):
            return
            
        logging.debug('decode cmd 4c')
        self.data_decode_dict = {}
        self.data_decode_dict['RCCONTROL_ADDR'] = hex_data[DATA_SA] + (hex_data[DATA_EA] & 0xf0) << 8
        self.data_decode_dict['MAIN_ADDR'] = hex_data[DATA_DA] + (hex_data[DATA_EA] & 0x0F) << 8
        self.data_decode_dict['DATA_LEN'] = len(hex_data) - 5
        self.data_decode_dict['DATA_CMD'] = hex_data[DATA_CMD]
        self.data_decode_dict['CMD_REPLAY'] = (hex_data[DATA_CC] - 0x10) & 0x01
        self.data_decode_dict['CMD_FORMATE'] = (hex_data[DATA_CC] - 0x10) & (1 << 2)
        self.data_decode_dict[SYSTEM_MODE] = hex_data[6] & 0x07
        
        # check 4c type  temp or windspeed or up_wind_dir or lr_wind_dir
        self.data_decode_dict[CMD_TYPE] = hex_data[6] & 0xf8

        self.data_decode_dict[WIND_SPEED] = hex_data[7] & (BIT6 + 0x07)

        self.data_decode_dict[WIN_DIR_UP] = hex_data[7] & 0x38

        self.data_decode_dict[SYS_TEMPT] = (hex_data[8] - 70 ) / 2

        self.data_decode_dict[WIN_DIR_LR] = hex_data[9] & 0x3f

    def decodeCmd81ResMain(self):
        logging.debug('decode cmd 81')

    def decodeCmd49ResMain(self):
        self.data_decode_rescmd49 = {}
        hex_data = self.data
        
        if (((hex_data[DATA_CC]&BIT1)  == BIT1) and (hex_data[DATA_CMD]!= 0x49)):
            logging.debug('data is not cmd49 res')
            return
        
        logging.debug('decode cmd RES 49')
        format_temp = (hex_data[DATA_CC]&(BIT2+BIT3)) >> 2
        logging.debug('format: {}'.format(format_temp))

        self.data_decode_rescmd49[ERROR_SYSTEM_NUM] = (hex_data[DATA_AU0]<<2 + (hex_data[DATA_AU1]&0xc0)>>6) - 0x20
        self.data_decode_rescmd49[ERROR_INDOOR_NUM] = hex_data[DATA_AU1]&0x3F
        self.data_decode_rescmd49[ERROR_CODE] = hex_data[DATA_AN] 
        
    
        
            





        


