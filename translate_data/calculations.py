
def visual_cash(block: list):
    for x in block:
        if x.cash_register is True and x.cash is False:
            print(f'\033[31m{x}\033[0m')

def summ_quarter(block):
    dict_quarter = {}
    total = {}
    for index in range(len(block)):
        data_line = block[index]
        owner = data_line.owner
        year = data_line.date[:4]
        month = int(data_line.date[5:7])
        quarter = round((month + 1) / 3)  # получение квартала значению месяца
        status = data_line.status
        name = f'{owner},{year}K{quarter}'
        name_total = f'{owner}'
        if status is True:
            dict_quarter[name] = dict_quarter.setdefault(name, 0) + data_line.summa
            total[name_total] = total.setdefault(name_total, 0) + data_line.summa
        elif status is False:
            dict_quarter[name] = dict_quarter.setdefault(name, 0) - data_line.summa
            total[name_total] = total.setdefault(name_total, 0) - data_line.summa
        else:
            print('неверный статус операции')

        #print(year, quarter, data_line)
    for key, value in dict_quarter.items():
        print(key, round(value, 2))

    print('----------------------------------------------------')

    print(f'общая сумма за весь период B={round(total["B"], 2)}')
    print(f'общая сумма за весь период K={round(total["K"], 2)}')


def summ_cash_register_quarter(block):
    dict_quarter = {}
    total = {}
    for index in range(len(block)):
        data_line = block[index]
        owner = data_line.owner
        year = data_line.date[:4]
        month = int(data_line.date[5:7])
        quarter = round((month + 1) / 3)  # получение квартала значению месяца
        status = data_line.status
        if data_line.cash_register is True:
            if data_line.cash is True:
                name = f'{owner}/{year}K{quarter}/наличкой'
            if data_line.cash is False:
                name = f'{owner}/{year}K{quarter}/без нал.'

            name_quarter = f'{owner}/{year}K{quarter}/итого:'
            name_total = f'{owner}'
            if status is True:
                dict_quarter[name] = dict_quarter.setdefault(name, 0) + data_line.summa
                dict_quarter[name_quarter] = dict_quarter.setdefault(name_quarter, 0) + data_line.summa
                total[name_total] = total.setdefault(name_total, 0) + data_line.summa
            elif status is False:
                dict_quarter[name] = dict_quarter.setdefault(name, 0) - data_line.summa
                dict_quarter[name_quarter] = dict_quarter.setdefault(name_quarter, 0) - data_line.summa
                total[name_total] = total.setdefault(name_total, 0) - data_line.summa
            else:
                print('неверный статус операции')
            #print(f'\031[31m{data_line}\033[0m')
    list_cash_box = []
    set_a = set()
    for key, value in dict_quarter.items():

        list_a = key.split('/')+[round(value,2)]
        list_cash_box.append(list_a)
    sorted_list = sorted(list_cash_box, key=lambda x: x[1])
    print(total)
    print('----------------------------------------------------')
    #print(list_cash_box)
    #print(sorted_list)
    summ =0
    for x in sorted_list:
        if x[2] == 'без нал.' and x[1]!='2022K3' and x[1]!='2019K3':
            summ+= x[3]
            print(x)
    print(f' сумма безнала ={summ}')



def summ_bank_account(block):
    bank_account = {}
    for index in range(len(block)):
        data_line = block[index]
        owner = data_line.owner
        year = data_line.date[:4]
        month = int(data_line.date[5:7])
        quarter = round((month + 1) / 3)  # получение квартала значению месяца
        status = data_line.status
        settlement_bank = data_line.settlement_bank
        name = f'{settlement_bank}'

        if status is True and settlement_bank is not None:
            bank_account[name] = bank_account.setdefault(name, 0) + data_line.summa
        if status is False and settlement_bank is not None:
            bank_account[name] = bank_account.setdefault(name, 0) - data_line.summa
        # else:
        #    print('неверный статус операции')
    for key, value in bank_account.items():
        print(key, round(value, 2))
