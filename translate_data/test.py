# -*- coding:utf8 -*-
def test_payment_doc(block: dict):  # тестирование по дате
    for key, value in block.items():
        print(key, value)


def test_list_date(block: list, date: str):  # тестирование по дате
    for line in block:
        if line[6] == date:
            print(line)


def test_list(block: list):  # вывод всего массива данных для теста
    b, x, k, n = 0, 0, 0, 0

    for line in block:
        print(line)
        # счетчик обработанных платежек в банк
        if line[0] == 'B':
            b += 1
        if line[0] == 'X':
            x += 1
        if line[0] == 'K':
            k += 1
        if not (line[0] == 'K' or line[0] == 'X' or line[0] == 'B'):
            n += 1
    print('X=', x, '\nK=', k, '\nB=', b, '\nN=', n)


def test_dict(company_dict: dict):  # отображает не распределенные компании по менеджерам
    for key, value in dt.dict_company.items():
        if not (value == 'K' or value == 'B'):
            print(key, value)


def test_data(block: list, data_start: str, data_end=''):
    print('-----------find------------------------------------')
    if data_end == '':
        data_end = data_start
    for line in block:
        if line[6] >= data_start and line[6] < data_end:
            print(line)
    print('-----------end find---------------------------------')
