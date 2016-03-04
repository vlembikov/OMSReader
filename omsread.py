# -*- coding: utf-8 -*-
#


from smartcard.System import readers
from smartcard.scard import *
import smartcard.util
import json

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
    print zn1
    return (zn1)

answer = {}.fromkeys(['ok', 'msg', 'data'])

# --- подключаемся к риделу ---
r = readers()
try:
    reader = r[0]
except IndexError:
    answer['ok'] = 0
    answer['msg'] = u'Подключите считыватель'
    print answer['msg']
    raise SystemExit
    
connection = reader.createConnection()
try:
    connection.connect()
except smartcard.Exceptions.CardConnectionException:
    answer['ok'] = 0
    answer['msg'] = u'Проверьте карту'
    print answer['msg']
    raise SystemExit

answer = {}.fromkeys(['ok', 'msg', 'data'])
# --- выбираем неизменяемые данные --- 
SELECT_DIR_CONST =  [0x00, 0xa4, 0x04, 0x0c, 0x07, 0x46, 0x4f, 0x4d, 0x53, 0x5f, 0x49, 0x44]
SELECT_FILE_CONST = [0x00, 0xa4, 0x02, 0x0c, 0x02, 0x02, 0x01]
READ_FILE_CONST = [0x00, 0xb0, 0x00, 0x00, 0x00]
data, sw1, sw2 = connection.transmit(SELECT_DIR_CONST)
# --- далее проверяется тип карты ---
if sw1 != 144 and sw2 != 0:
    answer['ok'] = 0
    if sw1 == 0x6a:
        answer['msg'] = u'Карта не поддерживается'
        print answer['msg']
    else:
        answer['msg'] = u'Неизвестная ошибка'
        print answer['msg']
    raise SystemExit

data, sw1, sw2 = connection.transmit(SELECT_FILE_CONST)
data_const, sw1, sw2 = connection.transmit(READ_FILE_CONST)
# --- выбираем изменяемые данные --- 
SELECT_DIR_CHANGE =  [0x00, 0xa4, 0x04, 0x0c, 0x07, 0x46, 0x4f, 0x4d, 0x53, 0x5f, 0x49, 0x4e, 0x53]
READ_DIR_CHANGE = [0x00, 0xca, 0x01, 0xb0, 0x02] # данная команда позволяет определить файл с актуальной информацией
data, sw1, sw2 = connection.transmit(SELECT_DIR_CHANGE)
data, sw1, sw2 = connection.transmit(READ_DIR_CHANGE) # имя нужного файла передается в двух байтах, которые мы добавляем в конец списка
SELECT_FILE_CHANGE = [0x00, 0xa4, 0x02, 0x0c, 0x02]
SELECT_FILE_CHANGE.append(data[0])
SELECT_FILE_CHANGE.append(data[1])
data, sw1, sw2 = connection.transmit(SELECT_FILE_CHANGE)
READ_FILE_CHANGE = [0x00, 0xb0, 0x00, 0x00, 0x00]
data_change, sw1, sw2 = connection.transmit(READ_FILE_CHANGE)

print "Прямая печать того, что пишется: "
dict_data = {
    'pol_ser': None,
    'pol_num': read_tag(data_const, 0x5f, 0x26),
    'policy': read_tag(data_const, 0x5f, 0x26),
    'family': read_tag(data_const, 0x5f, 0x21),
    'name': read_tag(data_const, 0x5f, 0x22),
    'patr': read_tag(data_const, 0x5f, 0x23),
    'sex': read_tag(data_const, 0x5f, 0x25),
    'bdate': read_tag(data_const, 0x5f, 0x24),
    'country_code': read_tag(data_const, 0x5f, 0x31),
    'country': read_tag(data_const, 0x5f, 0x32),
    'snils': read_tag(data_const, 0x5f, 0x27),
    'dataend': read_tag(data_const, 0x5f, 0x28),
    'bplace': read_tag(data_const, 0x5f, 0x29),
    'data_make_oms': read_tag(data_const, 0x5f, 0x2a),
    'fimg': read_tag(data_const, 0x5f, 0x41),
    'img': read_tag(data_const, 0x5f, 0x42),
    'ogrn': read_tag(data_change, 0x5f, 0x51),
    'okato': read_tag(data_change, 0x5f, 0x52),
    'data_start_insurance': read_tag(data_change, 0x5f, 0x53),
    'data_end_insurance': read_tag(data_change, 0x5f, 0x54)
    #'ecp': read_tag(data_change, 0x5f, 0x61)
    }

#print read_tag(data_const, 0x5f, 0x26)

#print json.dumps(dict_data, sort_keys=True)
answer['ok'] = 1
answer['msg'] = u'Успешно'
answer['data'] = dict_data 
print "Печать дампа: "
print json.dumps(answer, sort_keys=True)
#print answer