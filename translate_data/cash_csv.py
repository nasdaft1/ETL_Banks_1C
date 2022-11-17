# -*- coding:utf8 -*-
# для расчета сумм поступающих через кассу
# обрабатываем данные их выгруженных их другой программы и добавляем в dict_list_company
import dict_list_company as dt
import line_data as ld
import csv

def m(value):
    return str(value).replace(".", ",")

def d(x_dict:dict,key):
    value = x_dict.setdefault(key,0)
    return str(value).replace(".", ",")


def read_csv():
    data = {}
    total = {}
    with open('C:\\report\\report_tax.csv', mode='r', encoding='utf8') as file:
        file_reader = csv.reader(file, delimiter=';')
        for read_line in file_reader:
            # обрабатываем только наличные так как безнал ранее обрабатывался при работе с расчетным счетом
            cash_type = read_line[5]
            if cash_type == 'Тип оплаты':  # убрать строку с названием полей
                continue
            if cash_type == 'Электронными':
                cash_type = 'Безналичными'
            month = read_line[0][3:5]
            if month == '01' or month == '02' or month == '03': quarter = '1'
            if month == '04' or month == '05' or month == '06': quarter = '2'
            if month == '07' or month == '08' or month == '09': quarter = '3'
            if month == '10' or month == '11' or month == '12': quarter = '4'
            year = read_line[0][6:10]
            #           print(year, quarter, read_line[0],read_line[2],read_line)
            dates = f'{year}г. {quarter} [{cash_type}] квартал'
            dates_v = f'{year}г. {quarter} [{cash_type}] квартал возврат'
            dates_t = f'[{cash_type}]'

            if read_line[6] == 'Приход':
                data[dates] = data.setdefault(dates, 0) + float(read_line[2])
                total[dates_t] = total.setdefault(dates_t, 0) + float(read_line[2])
                # print(f'{read_line[0][:10]}, {read_line[2]}')
            elif read_line[6] == 'Возврат прихода':
                data[dates_v] = data.setdefault(dates_v, 0) - float(read_line[2])
                total[dates_t] = total.setdefault(dates_t, 0) - float(read_line[2])
                # print(f'{read_line[0][:10]},-{read_line[2]}')
            else:
                print('--ERROR---------------------------------------')
        file.close()

    for key, value in data.items():
        print(key, value)

    print(total)


def read_csv_list():
    data = {}
    total = {}
    product_dict = {}
    product_dict_2019 = {}
    product_dict_2020 = {}
    product_dict_2021 = {}
    product_dict_2022 = {}

    product_price_dict = {}

    with open('C:\\report\\report_tax.csv', mode='r', encoding='utf8') as file:
        file_reader = csv.reader(file, delimiter=';')
        for read_line in file_reader:
            # обрабатываем только наличные так как безнал ранее обрабатывался при работе с расчетным счетом
            cash_type = read_line[5]
            if cash_type == 'Тип оплаты':  # убрать строку с названием полей
                continue
            if cash_type == 'Электронными':
                cash_type = 'Безналичными'
            dates = f'{read_line[0][:10]}'

            dates_t = f'[{cash_type}]'
            year = read_line[0][6:10]
            product_name = f'{read_line[1]}'
            product_dict[product_name] = product_dict.setdefault(product_name, 0) + float(read_line[2])
            if year == '2019':
                product_dict_2019[product_name] = product_dict_2019.setdefault(product_name, 0) + float(read_line[2])
            if year == '2020':
                product_dict_2020[product_name] = product_dict_2020.setdefault(product_name, 0) + float(read_line[2])
            if year == '2021':
                product_dict_2021[product_name] = product_dict_2021.setdefault(product_name, 0) + float(read_line[2])
            if year == '2022':
                product_dict_2022[product_name] = product_dict_2022.setdefault(product_name, 0) + float(read_line[2])

            product_price_dict[product_name] = read_line[3]

            if cash_type == 'Безналичными':
                if read_line[6] == 'Приход':
                    data[dates] = data.setdefault(dates, 0) + float(read_line[2])
                    total[dates_t] = total.setdefault(dates_t, 0) + float(read_line[2])
                    # print(f'{read_line[0][:10]}, {read_line[2]}')
                elif read_line[6] == 'Возврат прихода':
                    data[dates] = data.setdefault(dates, 0) - float(read_line[2])
                    total[dates_t] = total.setdefault(dates_t, 0) - float(read_line[2])
                    # print(f'{read_line[0][:10]},-{read_line[2]}')
                else:
                    print('--ERROR---------------------------------------')
        file.close()

    for key, value in data.items():
        print(f'{key}\t{str(value).replace(".", ",")}')

    print(total)
    product_sort = dict(sorted(product_dict.items(), key=lambda x: x[1]))


    for key, value in product_sort.items():
        #print(f'{key}\t{str(value).replace(".", ",")}\t{str(product_price_dict[key]).replace(".", ",")}')
        print(f'{key}\t{d(product_dict_2019,key)}\t{d(product_dict_2020,key)}\t'
              f'{d(product_dict_2021,key)}\t{d(product_dict_2022,key)}\t{m(value)}\t'
              f'{d(product_price_dict,key)}')
        # print(f'{key}\t{product_dict_2019.setdefault(key, 0)}\t{product_dict_2020.setdefault(key, 0)}\t'
        #       f'{product_dict_2021.setdefault(key, 0)}\t{product_dict_2022.setdefault(key, 0)}\t{str(value).replace(".", ",")}\t'
        #       f'{str(product_price_dict[key]).replace(".", ",")}')

    # print(product_dict_2019)
    # print(product_dict_2020)
    # print(product_dict_2021)
    # print(product_dict_2022)



read_csv_list()
