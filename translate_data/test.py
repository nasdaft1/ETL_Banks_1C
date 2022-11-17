# -*- coding:utf8 -*-
# def test_payment_doc(block: dict):  # тестирование по дате
#    for key, value in block.items():
#        print(key, value)


# def test_list_date(block: list, date: str):  # тестирование по дате
#    for line in block:
#        if line[6] == date:
#            print(line)


# def test_dict(company_dict: dict):  # отображает не распределенные компании по менеджерам
#    for key, value in dt.dict_company.items():
#        if not (value == 'K' or value == 'B'):
#            print(key, value)


# def test_data(block: list, data_start: str, data_end=''):
#    print('-----------find------------------------------------')
#    if data_end == '':
#        data_end = data_start
#    for line in block:
#        if line[6] >= data_start and line[6] < data_end:
#            print(line)
#    print('-----------end find---------------------------------')

# f = [16300, -25, -25, -10337.98, 1000, -978, 1000, 29900, -8811.6, -4069, -1371, -25, -25, -25, 1000, 45452.5, -10690,
#      -8254, -25, -25, -60, -1794, -60, -2727.15, -6688,
#      -25, -21039.37, -25, -8254, -8100.34, -25, -25, -433, -25, -22439.62, -295, -25, -25, -25, 900, 1000, 20000, 900,
#      -33016, -25, 40000, -6690.85, -25, -435.35, -25,
#      30000, -10968.35, -6329, -25, -25, 8000, -864, -25, -54, -60, -54, -1800, -480, -6171.25, 18000, 1000, -7909.7,
#      -4669.4, -100, -5675.89, -25, -1381,
#      -25, 19000, 1000, -15819.4, -25, -8012.47, -5404.8, -25, -25, 20000, -1080, -60, -1140, -60, 19000, -22305.68, -25,
#      19000, 10000, -1140, -1140, -600,
#      -1200, 45000, -4636.22, -25, -16322, -25, 13850, -7259, -4638.02, -25, -25, 16000, -16189.8, -25, -2700, -831,
#      -960, -4986.47, -25, -1500, -25, -2750,
#      -25, -800, -25, 40000, -16189.8, -25, -12659, -1296.94, -25, -25, 30000, 41000, -13286.22, -5307, -25, -25, -25,
#      -2400, -1800, -2460, 23680, -17037.26,
#      -25, 17000, -8518.63, -25, 12000, -2427, -25, 12000, -6482.63, -25, 4000, -7900, -25, -1420.8, -1020, -720, -720,
#      -240
#      ]


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
        # y = dict(block[line])
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
        if key == None:
            print(y)


# def test_data_summ_x(obj_status, obj_summa, value):
#    if (obj_status is not None) and (obj_summa is not None):
#        if obj_status is True:
#            # print(f'{obj_status}, {obj_summa}, {value}')
#            return obj_summa + value
#        if obj_status is False:
#            # print(f'{obj_status}, {obj_summa}, -{value}')
#            return obj_summa - value


def test_data_summ1(block, data_start, data_end, owner_value: str = None):
    summa = 0.0
    summa_z = 0.0
    summa_old = 0.0
    summ = {}
    for line in range(len(block)):
        y = block[line]
        if (data_start <= y.date) and (y.date <= data_end):
            owner_op = y.owner
            print(summa_z, summa_old)
            # summa = test_data_summ_x(y.status, summa, y.summa)

            # if owner_value is None:
            #    if y.status is True:
            #        summ[y.owner] = summ.setdefault(y.owner, 0) + y.summa
            #    if y.status is False:
            #        summ[y.owner] = summ.setdefault(y.owner, 0) - y.summa
            #    print(summ.setdefault(y.owner, 0), y)
            if owner_op == 'B':  # owner_value:

                status_op = y.status
                summa_value = y.summa
                summa_old = summa_z
                if status_op is True:
                    summa_z += summa_value
                if status_op is False:
                    summa_z -= summa_value
                    # if (y.netting is None):
                    print(summa_old, summa_value, summa_z, y)
    # summa_x = round(summa - summa_b - summa_k, 2)
    print(f'Сумма общая за перидод с {data_start} до {data_end} = {summa}')
    if owner_value is None:
        for key, value in summ.items():
            print(f'Сумма владельца "{key}" за перидод с {data_start} до {data_end} = {value}')
    if owner_value is not None:
        print(f'Сумма владельца {owner_value} за перидод с {data_start} до {data_end} = {summa_z}')
    return summa


def test_data_summ(block, data_start, data_end, owner_value: str = None):
    summa = 0.0
    summa_z = 0.0
    summa_old = 0.0
    for line in range(len(block)):
        y = block[line]
        if (data_start <= y.date) and (y.date <= data_end):
            owner_op = y.owner

            if owner_op == owner_value:  # owner_value:
                summa_value = y.summa
                status_op = y.status
                summa_old = summa_z
                if status_op is True:
                    summa_value *= 1
                if status_op is False:
                    summa_value *= -1
                summa_z += summa_value
                # print(status_op,summa_value)
                # if y.status is False and y.netting is None:
                print(round(summa_old, 2), round(summa_value, 2), round(summa_z, 2), y)
                if (summa_old + summa_value) != summa_z:
                    print('ERROR-----------------------------------')
    print(f'Сумма общая за перидод с {data_start} до {data_end} = {summa}')
    if owner_value is not None:
        print(f'Сумма владельца {owner_value} за перидод с {data_start} до {data_end} = {summa_z}')
    return summa


def test_data_summ1(block):
    summa_all = 0
    data_dict = {}
    for line in range(len(block)):
        data_line = block[line]
        name = data_line.owner + ' ' + data_line.date[:4]
        name_s = '- ' + data_line.date[:4]
        summa = data_line.summa
        if data_line.status is True:
            data_dict[name] = data_dict.setdefault(name, 0) + summa
            data_dict[name_s] = data_dict.setdefault(name_s, 0) + summa
            summa_all += summa
        else:
            data_dict[name] = data_dict.setdefault(name, 0) - summa
            data_dict[name_s] = data_dict.setdefault(name_s, 0) - summa
            summa_all -= summa
    print(data_dict)
    for key, value in data_dict.items():
        print(key, value)
    print('summa all=', summa_all)


def test_data_summ2(block):
    summa_all = 0
    data_dict = {}
    for line in range(len(block)):
        data_line = block[line]
        name = data_line.owner + ' ' + data_line.date[:4]
        name_s = '- ' + data_line.date[:4]
        summa = data_line.summa
        if data_line.status is True:
            data_dict[name] = data_dict.setdefault(name, 0) + summa
            data_dict[name_s] = data_dict.setdefault(name_s, 0) + summa
            summa_all += summa
        else:
            data_dict[name] = data_dict.setdefault(name, 0) - summa
            data_dict[name_s] = data_dict.setdefault(name_s, 0) - summa
            summa_all -= summa
    print(data_dict)
    for key, value in data_dict.items():
        print(key, value)
    print('summa all=', summa_all)


def test_data_quarter_summ(block):  # поквартальный доход
    quarter_dict = {1: 1, 2: 1, 3: 1,
                    4: 2, 5: 2, 6: 2,
                    7: 3, 8: 3, 9: 3,
                    10: 4, 11: 4, 12: 4}
    # доход год, месяц, дата уплаты налога,
    taxes = [
        [[[2019, 1]], '2019.04', '1к2019'],
        [[[2019, 2]], '2019.07', '2к2019'],
        [[[2019, 3]], '2019.10', '3к2019'],
        [[[2019, 4]], '2020.03', '4к2019'],
        [[[2020, 1]], '2020.05', '1к2020'],
        [[[2020, 2], [2020, 3]], '2020.10', '3к2020'],
        [[[2020, 4], [2021, 1]], '2021.04', '4к2020 1к2021'],
        [[[2021, 2]], '2021.07', '2к2021'],
        [[[2021, 3]], '2021.10', '3к2021'],
        [[[2021, 4]], '2022.03', '4к2021'],
        [[[2022, 1]], '2022.04', '1к2022']
    ]

    taxes_move = {}

    year_transition_tax = 2019

    summa_all = 0
    data_dict = {}
    for line in range(len(block)):
        data_line = block[line]
        year = int(data_line.date[:4])
        if year >= year_transition_tax:
            month = int(data_line.date[5:7])
            year_mounth = data_line.date[:7]

            quarter = quarter_dict.setdefault(month, None)
            summa = data_line.summa
            name = data_line.owner
            status = data_line.status
            for i in taxes:
                for n in i[0]:
                    if year == n[0] and quarter == n[1]: # получить поквартальное суммирование доходов
                        if name == 'B' or name == 'K':
                            name_profit = name + f'  {i[1]} {i[2]} доход'
                            name_expenses = name + f'  {i[1]} {i[2]} расход'
                            if status is True:
                                data_dict[name_profit] = data_dict.setdefault(name_profit, 0) + summa
                            if status is False:
                                data_dict[name_expenses] = data_dict.setdefault(name_expenses, 0) - summa
                            if status is None:
                                print('неверный статус операции')
                if year_mounth == i[1] and name == 'B2': # обработка отчислений налогов
                    print(year_mounth, i[1], data_line)
                    name_profit = name + f' {i[1]} {i[2]} доход'
                    name_expenses = name + f' {i[1]} {i[2]} расход'
                    if status is True:
                        data_dict[name_profit] = data_dict.setdefault(name_profit, 0) + summa
                    if status is False:
                        data_dict[name_expenses] = data_dict.setdefault(name_expenses, 0) - summa
                    if status is None:
                        print('неверный статус операции')

    for key, value in data_dict.items():
        if key.find('доход') > -1 or key[:2] == 'B2':
            data = key[3:10]
            taxes_move[data] = taxes_move.setdefault(data, {})
            taxes_move[data][key[:2]] = value
            taxes_move[data]['i'] = data
            taxes_move[data]['yq'] = key[11:17]
    for key, value in taxes_move.items():
        print(key, value)
        k = value.setdefault('K ')
        b = value.setdefault('B ')
        b2 = value.setdefault('B2')
        x =k*b2/(k+b)
        print('K компенсация по налогам В', x)
    print('summa all=', summa_all)


def test_data_quarter_summ1(block):  # поквартальный доход
    quarter_dict = {1: 1, 2: 1, 3: 1,
                    4: 2, 5: 2, 6: 2,
                    7: 3, 8: 3, 9: 3,
                    10: 4, 11: 4, 12: 4}
    taxes = [
        [[[2019, 1]], '2019.04', {}],
        [[[2019, 2]], '2019.07', {}],
        [[[2019, 3]], '2019.10', {}],
        [[[2019, 4]], '2020.03', {}],
        [[[2020, 1]], '2020.05', {}],
        [[[2020, 2], [2020, 3]], '2020.10', {}],
        [[[2021, 1], [2020, 4]], '2021.04', {}],
        [[[2021, 2]], '2021.07', {}],
        [[[2021, 3]], '2021.10', {}],
        [[[2021, 4]], '2022.03', {}],
        [[[2022, 1]], '2022.04', {}]
    ]
    year_transition_tax = 2019

    summa_all = 0
    data_dict = {}
    for line in range(len(block)):
        data_line = block[line]
        year = int(data_line.date[:4])
        if year >= year_transition_tax:
            month = int(data_line.date[5:7])
            year_mounth = data_line.date[:7]

            quarter = quarter_dict.setdefault(month, None)
            summa = data_line.summa

            status = data_line.status

            name_profit = data_line.owner + f' {quarter} квартал {year} доход'
            name_expenses = data_line.owner + f' {quarter} квартал {year} расход'
            if status is True:
                data_dict[name_profit] = data_dict.setdefault(name_profit, 0) + summa
            if status is False:
                data_dict[name_expenses] = data_dict.setdefault(name_expenses, 0) - summa
            if status is None:
                print('неверный статус операции')

    for key, value in data_dict.items():
        if key.find('доход') > -1 or key[:2] == 'B2':
            print(key, value)
    print('summa all=', summa_all)


def test_visual_None(block):
    for line in range(len(block)):
        y = block[line]
        if y.summa is None:
            print(y)


def com(block):
    comp = {}
    s = ''
    for line in block:
        comp[line.payment_purpose] = line.owner
        s = line.payment_purpose
        s.upper()
        if s.find('ОХРАННОЙ') != -1:
            print(s)
            print(line)

    for key, value in comp.items():
        if key.find('ОХРАННОЙ') != -1:
            print(f"'{key}':{value}")
            print(line)
