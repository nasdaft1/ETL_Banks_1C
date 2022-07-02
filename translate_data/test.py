# -*- coding:utf8 -*-
#def test_payment_doc(block: dict):  # тестирование по дате
#    for key, value in block.items():
#        print(key, value)


#def test_list_date(block: list, date: str):  # тестирование по дате
#    for line in block:
#        if line[6] == date:
#            print(line)


#def test_dict(company_dict: dict):  # отображает не распределенные компании по менеджерам
#    for key, value in dt.dict_company.items():
#        if not (value == 'K' or value == 'B'):
#            print(key, value)


#def test_data(block: list, data_start: str, data_end=''):
#    print('-----------find------------------------------------')
#    if data_end == '':
#        data_end = data_start
#    for line in block:
#        if line[6] >= data_start and line[6] < data_end:
#            print(line)
#    print('-----------end find---------------------------------')


def test_values(v1, v2, v3, v4, v5, v6, v7):
    l = [v1, v2, v3, v4, v5, v6, v7]
    for x in range(2, 7):
        if l[x - 1] != 'X' and l[x] == 'X':
            return 'error'
    return 'ok'


def test_find(block: list, name: str, value: str, type_find: bool):
    """
    :param block: list = список словарей
    :param name: str = ключ ко которому будет осуществляться поиск
    :param value: str = значения по которому будет осуществлятся поиск
    :param type_find: bool = False - поиск осуществляется по точному совпадению
                             True- поиск осуществляется по фрагменту текста value
    :return: None
    """
    line_sum = len(block)
    line_n = 0
    for line in range(line_sum):
        y = dict(block[line])
        if type_find == False:
            value_r = y.setdefault(name, None)
            if value == value_r:
                print(y)
                line_n += 1

        else:
            value_r = str(y.setdefault(name, None))
            if (value_r is not None) and (value_r.find(value) != -1):
                print(y)
                line_n += 1
    print('Количество отфильтрованных строк =', line_n)


def test_owner(block):
    """
    :param block: список словарей со значениями кому пренадлежит платежка
    """
    d = {}
    line_sum = len(block)
    for line in range(line_sum):
        #y = dict(block[line])
        y = block[line]
        y1 = y.owner
        d[y1] = d.setdefault(y1, 0) + 1
    print(d)
    print('Всего = ', line_sum)


def test_visual(block, key: str = None):
    for line in range(len(block)):
        y = block[line]

        if y.owner == key:
            print(y)

