import line_data as ld
import dict_list_company as dl



def pivot(data_dict: dict) -> dict:
    taxes_move = {}
    for key, value in data_dict.items():
        list_key = key.split('/')
        if list_key[3] == 'доход' or list_key[0] == 'B2':
            data = list_key[1]
            taxes_move[data] = taxes_move.setdefault(data, {})
            taxes_move[data][list_key[0]] = abs(value)
            taxes_move[data]['yq'] = list_key[2]
    return taxes_move


def separation(taxes_move: dict) -> dict:  # добаление в словарь
    for key, value in taxes_move.items():
        k = value.setdefault('K')
        b = value.setdefault('B')
        b2 = value.setdefault('B2')
        name_operation = value.setdefault('yq')
        x = round((k * b2 / (k + b)), 2)
        taxes_move[key]['Kt'] = x
        print(key, value)
    return taxes_move


def update_data_dict(data_dict: dict, data_line, i)-> dict:
    summa = data_line.summa
    name = data_line.owner
    status = data_line.status
    name_profit = name + f'/{i[1]}/{i[2]}/доход'
    name_expenses = name + f'/{i[1]}/{i[2]}/расход'
    if status is True:
        data_dict[name_profit] = data_dict.setdefault(name_profit, 0) + summa
    if status is False:
        data_dict[name_expenses] = data_dict.setdefault(name_expenses, 0) - summa
    if status is None:
        print('неверный статус операции')
    return data_dict


def comp_data_line(owner: str, date: str, status: bool, value_sep: dict):
    data_line = ld.LineData()
    data_line.owner = owner
    data_line.date = date
    data_line.payment_purpose = value_sep['yq']
    data_line.status = status
    data_line.summa = value_sep['Kt']
    data_line.netting = True
    data_line.cash = False
    data_line.tax =True
    return data_line


def compensation(block: list, sep: dict) -> list:
    sep_list = list(sep)  #
    value_date_old = '2060.01.01'  # максимальная дата до которой возможно будет существовать фирма
    for line in range(len(block) - 1, 0, -1):
        data_line = block[line]
        value_data_line = data_line.date
        for sep_line in sep_list:
            value_data_sep = sep_line + '.28'
            if value_data_line <= value_data_sep and value_data_sep < value_date_old:
                value_sep = sep[sep_line]
                block.insert(line + 1, comp_data_line('B3', value_data_sep, True, value_sep))
                block.insert(line + 1, comp_data_line('K3', value_data_sep, False, value_sep))
                sep_list.remove(sep_line)
        value_date_old = value_data_line
    return block


def data_quarter_summ(block: list) -> list:   # поквартальный доход
    year_transition_tax = 2019  # дата перехода на УСН доход - расход
    data_dict = {}
    for line in range(len(block)):
        data_line = block[line]
        year = int(data_line.date[:4])
        if year >= year_transition_tax:
            month = int(data_line.date[5:7])
            year_mounth = data_line.date[:7]
            quarter = round((month + 1) / 3)  # получение квартала значению месяца
            name = data_line.owner
            for date_taxes in dl.taxes: # из файла словаря
                for n in date_taxes[0]:
                    if year == n[0] and quarter == n[1]:  # получить поквартальное суммирование доходов
                        if name == 'B' or name == 'K':
                            data_dict = update_data_dict(data_dict, data_line, date_taxes)
                if year_mounth == date_taxes[1] and name == 'B2':  # обработка отчислений налогов
                    data_dict = update_data_dict(data_dict, data_line, date_taxes)
    taxes_move = pivot(data_dict) # разворот словаря
    sep = separation(taxes_move) # подсчет компенсации налова на основание процента дохода за отчетный период между хозяйствующими субъектами
    block = compensation(block, sep) # внесение в список транзакций операций ,компенсации налогов между хоз. субъектами

    #block = visual(block)
    return block

