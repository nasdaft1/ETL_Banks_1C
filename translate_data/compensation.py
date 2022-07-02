# -*- coding:utf8 -*-
import dict_list_company as dt

def x(line_dict: dict):
    del line_dict['ПлательщикИНН=']
    del line_dict['ПолучательИНН=']
    line_dict['Плательщик1='] = 'K'
    line_dict['Получатель1='] = 'B'
    line_dict_credit = line_dict.copy()
    line_dict_debit = line_dict.copy()
    # line_dict_debit['Статус='] = 'Debit'
    # sum = float(line_dict.setdefault('Сумма=', None))
    #for x in range(len( dt.list_date_owner)):

    return line_dict


def compensation(block: list):
    # модификация данных для компенсации между хозяйствующими субъектами
    # добавление транзакций по перемещению денежных срездст между виртуальными счетами

    for line in range(len(block) - 1, 0, -1):
        line_dict = dict(block[line])
        value_owner = line_dict.setdefault('Владелец=', None)
        if value_owner == 'O':
#            print(line_dict)
            block.insert(line, x(line_dict))  # производим вставку в список операций взаиморасчетов x(line_dict)
    print(len(block))
    return block
