'''
Author: your name
Date: 2021-12-23 13:35:24
LastEditTime: 2021-12-26 12:53:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\rd505.py
'''

from os import stat
import pprint

IR_DATA_FC0 = 4
IR_DATA_FC1 = 5
IR_DATA_FC2 = 6
IR_DATA_FC3 = 7
IR_DATA_FC5 = 9
IR_DATA_FC6 = 10
IR_DATA_EFC0 = 13
IR_DATA_EFC1 = 14

BIT0 = 0x01
BIT1 = 0x02
BIT2 = 0x04
BIT3 = 0x08
BIT4 = 0x10
BIT5 = 0x20
BIT6 = 0x40
BIT7 = 0x80


IR_TYPE_LENGTH_A = 12
IR_TYPE_LENGTH_C = 6
IR_TYPE_LENGTH_D = 10
IR_TYPE_LENGTH_E = 11

class Rd505IrData():
    def __init__(self) -> None:
        self.onstate = 0

class Rd505IrProcess():
    def __init__(self) -> None:
        self.dat = Rd505IrData()
        self.irdict = {}
    

    def ir_typeB(self, hex_data):

        if self.typeb_check(hex_data) == 0:
            return
        #CHECK POWER STATE
        self.typeb_fc1_check_power(hex_data)
        self.typeb_fc1_fc2_runmode(hex_data)
        self.typeb_fc1_efc0_winspeed(hex_data)
        self.typeb_fc2_temperature(hex_data)
        self.typeb_fc5_ventilate(hex_data)
        self.typeb_fc6_up_and_down_wind(hex_data)
        self.typeb_fc6_left_and_right_wind(hex_data)
        self.typeb_efc0_econavi(hex_data)
        self.typeb_efc0_nanoe(hex_data)
        self.typeb_efc1_powersave(hex_data)
        
    def ir_typeE(self, hex_data):
        if self.typeE_check(hex_data) == 0:
            return
        self.ir_typeE_fc1_windspeed(hex_data)
        

    def ir_typeE_fc1_windspeed(self, hex_data):
        d1 = hex_data[IR_DATA_FC1]
        d2 = hex_data[IR_DATA_FC3]
        spec_windspeed = ''
        if (d1 == 0x07):
            if (d2):
                spec_windspeed = '超强'
            else:
                spec_windspeed = '超强超静关'
        if (d1 == 0x08):
            if (d2):
                spec_windspeed = '超静'
            else:
                spec_windspeed = '超强超静关'
        if (d1 == 0x09):
            self.irdict['LedDuty'] = d2
        
        self.irdict['SpecWinSpeed'] = spec_windspeed


    def decode_ir(self, strdata):
        fun_dict = {
            16 : self.ir_typeB,
            11 : self.ir_typeE
        }
        bit_data = string_to_listbytes(strdata)
        print('')
        print('data is: {}'.format(strdata))
        print('len is: ' + str(len(bit_data)))

        if ((bit_data[0]==0x40) and (bit_data[1]==0x00) and (bit_data[3]==0x81)):
            len_data = len(bit_data)
            fun_dict.get(len_data, self.ir_err_fun)(bit_data)
    
    def ir_err_fun(self, hex_data):
        print('ir err length：{}'.format(len(hex_data)))

    # check type e
    def typeE_check(self, hex_data):
        if (hex_data[2]!=0x14):
            print('PSC error')
            return 0
	    
        if (hex_data[IR_DATA_FC0]!=0x3F):
            print('TYPE FC0 error')
            return 0
        temp2 = hex_data[2]>>4
	
        for i in range(3, IR_TYPE_LENGTH_E - 1):
            temp2 += (hex_data[i] & 0x0f)
            temp2 += (hex_data[i] >> 4)

        if (temp2 != hex_data[IR_TYPE_LENGTH_E-1]):
            print('TYPE DC1 error')
            return 0

        return 1

    def typeb_check(self, hex_data):
        if (hex_data[2]!=0x14):
            print('TYPB PSC error')
            return 0
	    
        temp2 = hex_data[2]>>4
	
        for i in range(3, IR_TYPE_LENGTH_A - 1):
            temp2 += (hex_data[i] & 0x0f)
            temp2 += (hex_data[i] >> 4)

        if (temp2 != hex_data[IR_TYPE_LENGTH_A-1]):
            print('TYPB DC1 error')
            return 0
        
        for i in range(IR_TYPE_LENGTH_A-1, len(hex_data) - 1):
            temp2 += (hex_data[i]&0x0f)
            temp2 += (hex_data[i]>>4)

        if (temp2 != hex_data[len(hex_data)-1]):
            print('TYPB DC2 error')
            return 0

        return 1


    def typeb_fc1_check_power(self, hex_data):
        power_dict = {
            1 : '停止',
            2 : '运转'
        }
        state = hex_data[IR_DATA_FC1] &  (BIT0+BIT1)
        self.irdict['PowerState'] = power_dict.get(state, '无效位')

    # MODE 
    def typeb_fc1_fc2_runmode(self, hex_data):
        run_mode_dic = {
            0 : '送风',
            1 : '暖房',
            2 : '冷房',
            3 : '抽湿',
            4 : '自动'
        }
        d1 = (hex_data[IR_DATA_FC1]&(BIT6+BIT7))>>6
        d2 = (hex_data[IR_DATA_FC2]&BIT7)>>7
        state = (d2 << 2) + d1
        self.irdict['RunMode']=run_mode_dic.get(state, '无效位')

    # FUN SPEED
    def typeb_fc1_efc0_winspeed(self, hex_data):
        fun_mode_dic = {
            0 : '自动',
            1 : '急5',
            2 : '弱-1',
            3 : '强-3',
            6 : '弱+2',
            7 : '强+4'
        }
        d1 = (hex_data[IR_DATA_FC1]&(BIT2+BIT3))>>2
        d2 = (hex_data[IR_DATA_EFC0]&BIT4)>>4
        state = (d2 << 2) + d1
        self.irdict['FunMode']=fun_mode_dic.get(state, '无效位')


    # Temperature
    def typeb_fc2_temperature(self, hex_data):
        d1 = hex_data[IR_DATA_FC2]&0x3F
        state = 4+ (d1 >>1 )
        self.irdict['temperature'] = state
    
    # ventilate 换气
    def typeb_fc5_ventilate(self, hex_data):
        ventilate_dic = {
            1 : '换气ON',
            0 : '换气OFF'
        }
        d1 = (hex_data[IR_DATA_FC5]&BIT7)>>7
        state = d1
        self.irdict['ventilate'] = ventilate_dic.get(state, '无效位')

    # up and down wind 上下风向
    def typeb_fc6_up_and_down_wind(self, hex_data):
        up_down_wind_dic = {
            0 : '上下风向自动',
            1 : '上下风向1',
            2 : '上下风向2',
            3 : '上下风向3',
            4 : '上下风向4',
            5 : '上下风向5',
            7 : '上下风向停止'
        }
        d1 = hex_data[IR_DATA_FC6]&(BIT0+BIT1+BIT2)
        state = d1
        self.irdict['up_down_wind'] = up_down_wind_dic.get(state, '无效位')

    
    # left and right wind 左右风向
    def typeb_fc6_left_and_right_wind(self, hex_data):
        up_down_wind_dic = {
            0 : '左右风向自动',
            1 : '左右风向1',
            2 : '左右风向2',
            3 : '左右风向3',
            4 : '左右风向4',
            5 : '左右风向5',
            7 : '左右风向停止'
        }
        d1 = hex_data[IR_DATA_EFC0]&(BIT0+BIT1+BIT2)
        state = d1
        self.irdict['left_right_wind'] = up_down_wind_dic.get(state, '无效位')
    
    # ECONAVI
    def typeb_efc0_econavi(self, hex_data):
        econavi_dic = {
            1 : 'ECONAVI_ON',
            0 : 'ECONAVI_OFF'
        }
        d1 = (hex_data[IR_DATA_EFC0]&BIT5) >> 5
        state = d1
        self.irdict['econavi'] = econavi_dic.get(state, '无效位')

    # Nanoe
    def typeb_efc0_nanoe(self, hex_data):
        econavi_dic = {
            1 : 'Nanoe_ON',
            0 : 'Nanoe_OFF'
        }
        d1 = (hex_data[IR_DATA_EFC0] & BIT6) >> 6
        state = d1
        self.irdict['nanoe'] = econavi_dic.get(state, '无效位')

    # PowerSave 节能
    def typeb_efc1_powersave(self, hex_data):
        econavi_dic = {
            1 : '节能_ON',
            0 : '节能_OFF'
        }
        d1 = (hex_data[IR_DATA_EFC1]&BIT6) >> 6
        state = d1
        self.irdict['powersave'] = econavi_dic.get(state, '无效位')
    

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
        




