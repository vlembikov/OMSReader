# -*- coding: utf-8 -*-
#

from smartcard.System import readers
from smartcard.scard import *
import smartcard.util
import json
import re

DATA_KEYS = {
    'pol_ser': None,
    'pol_num': '5f26',
    'policy': '5f26',
    'family': '5f21',
    'name': '5f22',
    'patr': '5f23',
    'sex': '5f25',
    'bdate': '5f24',
    'country_code': '5f31',
    'country': '5f32',
    'snils': '5f27',
    'dataend': '5f28',
    'bplace': '5f29',
    'data_make_oms': '5f2a',
    'fimg': '5f41',
    'img': '5f42',
    'ogrn': '5f51',
    'okato': '5f52',
    'data_start_insurance': '5f53',
    'data_end_insurance': '5f54',
    #'ecp':'5f61'
    }

def bcd_to_int(bcd):
    """Decode a 2x4bit BCD to a integer.
    """
    out = 0
    for d in (bcd >> 4, bcd):
        for p in (1, 2, 4 ,8):
            if d & 1:
                out += p
            d >>= 1
        out *= 10
    return out / 10

def find2elements(data, arg1, arg2):
    count_list = len(data)
    i = 1
    index = -1
    while i < count_list:
        if data[i-1] == arg1 and data[i] == arg2:
            index = i
            break
        i = i+1
    return index

def read_tag(data, *tags):
    index = find2elements(data, tags[0], tags[1]);
    if index == -1:
        return None
    tagoflength = index+1
    startreadtag = index+2
    endreadtag = tagoflength+data[tagoflength]
    if data[tagoflength] == 1:
        if data[startreadtag] == 1:
            zn1 = True
        else:
            zn1 = False
    if data[tagoflength] == 4:
        zn1 = str(bcd_to_int(data[startreadtag+2])).zfill(2)+str(bcd_to_int(data[startreadtag+3])).zfill(2)+'-'+str(bcd_to_int(data[startreadtag+1])).zfill(2)+'-'+str(bcd_to_int(data[startreadtag])).zfill(2)
    if data[tagoflength] != 1 and data[tagoflength] != 4:
        zn1 = bytearray(data[startreadtag:endreadtag+1]).decode('utf8')
    return (zn1)

def read_data(args = None):
    if args is None or args =='null':
        args = ['pol_ser', 'pol_num', 'policy', 'family', 'name', 'patr', 'sex', 'bdate']
    if type(args) is str:
        s = args
        args = re.findall(r'[a-z]+_{0,1}[a-z]*_{0,1}[a-z]*',s)
        #args = s.split(", ")
    dict_data = {}.fromkeys(args)
    answer = {'ok': 0, 'msg': "Неизвестная ошибка в программе", 'data': dict_data}
    r = readers()
    try:
        reader = r[0]
        connection = reader.createConnection()
        try:
            connection.connect()
            SELECT_DIR_CONST =  [0x00, 0xa4, 0x04, 0x0c, 0x07, 0x46, 0x4f, 0x4d, 0x53, 0x5f, 0x49, 0x44]
            SELECT_FILE_CONST = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x02, 0x01]
            READ_FILE_CONST = [0x00, 0xb0, 0x00, 0x00, 0x00]
            data, sw1, sw2 = connection.transmit(SELECT_DIR_CONST)
            if sw1 != 144 and sw2 != 0:
                answer['ok'] = 0
                if sw1 == 0x6a:
                    answer['msg'] = u'Карта не поддерживается'
                else:
                    answer['msg'] = u'Неизвестная ошибка'
            data, sw1, sw2 = connection.transmit(SELECT_FILE_CONST)
            data_const, sw1, sw2 = connection.transmit(READ_FILE_CONST)
            SELECT_DIR_CHANGE =  [0x00, 0xa4, 0x04, 0x0c, 0x07, 0x46, 0x4f, 0x4d, 0x53, 0x5f, 0x49, 0x4e, 0x53]
            READ_DIR_CHANGE = [0x00, 0xca, 0x01, 0xb0, 0x02] 
            data, sw1, sw2 = connection.transmit(SELECT_DIR_CHANGE)
            data, sw1, sw2 = connection.transmit(READ_DIR_CHANGE) 
            SELECT_FILE_CHANGE = [0x00, 0xa4, 0x02, 0x0c, 0x02]
            SELECT_FILE_CHANGE.append(data[0])
            SELECT_FILE_CHANGE.append(data[1])
            data, sw1, sw2 = connection.transmit(SELECT_FILE_CHANGE)
            READ_FILE_CHANGE = [0x00, 0xb0, 0x00, 0x00, 0x00]
            data_change, sw1, sw2 = connection.transmit(READ_FILE_CHANGE)
            data = data_const + data_change
            for key in dict_data:
                if key == 'pol_ser':
                    dict_data[key] = None
                    continue
                param_str = DATA_KEYS[key]
                param1 = int(param_str[:2],16)
                param2 = int(param_str[2:4],16)
                dict_data[key] = read_tag(data, param1, param2)
            answer['ok'] = 1
            answer['msg'] = u'Успешно'
            answer['data'] = dict_data 
        except smartcard.Exceptions.CardConnectionException:
            answer['ok'] = 0
            answer['msg'] = u'Проверьте карту'
        except KeyError:     
            answer['msg'] = u'Поля нет на карте. Проверьте запрос'
        except Exception as inst:
            print type(inst)
            answer['msg'] = u'Пока не знаем, что это'
    except IndexError:
        answer['ok'] = 0
        answer['msg'] = u'Подключите считыватель'
    finally:
        return answer
