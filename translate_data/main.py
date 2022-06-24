# -*- coding:utf8 -*-
from time import perf_counter
import work_file as WF


def find_x(_owner: str, _number: str, _correction_list: list):
    if _owner == 'X':  # определяем не распределенные платежки банку за обслуживание платежей
        for position_x in _correction_list:
            if (position_x[1] == _number and position_x[0] != 'X'):
                return position_x[0]
    return _owner


def redistribution(block: list):
    _block_new = []
    for line in block:
        if line[0] == 'O':
            # print(line)
            line[0] = 'B'
            _block_new.append(line)
            # '6321125732'
            line[0] = 'N'
            line[8] = 1000
            line[11] = 'internally'
            _block_new.append(line)
        else:
            _block_new.append(line)
    #  обработать "ВАШ БУХГАЛТЕР"
    return _block_new


def payment_list(block: list, payment_doc: dict):
    # Для анализа обработанных и не обработанных платежей
    # При правельном распределении должно остаться N=0
    company_dict_N = {}  # словарь для неизвестных компаний

    o, b, x, k, n = 0, 0, 0, 0, 0
    for line in block:
        if line[0] == 'X':
            line_x = find_x(line[0], line[7], payment_doc.setdefault(line[6]))
            line[0] = line_x  # замена индикатора владельца виртуального счета

    for line in block:
        if (line[0] == 'O') or (line[0] == 'N'):
            print(line)
        # print(line)
        # производим расчет обработанных и не обработанных данных
        if line[0] == 'B':
            b += 1
        if line[0] == 'X':
            x += 1
        if line[0] == 'K':
            k += 1
        if line[0] == 'O':
            o += 1
        if not (line[0] == 'K' or line[0] == 'X' or line[0] == 'B' or line[0] == 'O'):
            # Составление словаря с контрагентами неизвестно кому пренадлежацими
            n += 1
            company_dict_N[line[4]] = 'N'
            company_dict_N[line[5]] = 'N'
    for key, value in company_dict_N.items():
        # распечатывание словаря с контрагентами неизвестно кому пренадлежацими
        print("'" + key + "':'" + value + "',")
    print(' Налоги X=', x, '\n Хозяйствующий субъект K=', k,
          '\n Хозяйствующий субъект B=', b, '\n Совместное использование O=', o, '\n Неизвестный хоз. субъект N=', n)


def sort_block(block: list):
    return sorted(block, key=lambda block: block[6])  # производим сортировку по полю дата в много мерном списке


def processing1(block: list):
    # блок для созадания взаимосвязи платежей и плата за прием и обработку платежных документов
    # для разделения виртуального разгранечения направления деятельности в фирме
    # Пример 2020.11.01 , 1, 2, 3   2020.11.02 1, 2, 3, 4, 5    2020.11.05  4, 5, 6
    line_list, line_list_old = [], []
    _date_old = ''
    payment = {}
    for line in block:
        _date = line[6]
        if _date == _date_old:
            line_list += [[line[0], line[7]]]
            payment[_date] = line_list  # вводится для того чтобы последнея дата была в словаре со значениями
        else:
            payment[_date_old] = line_list_old + line_list
            line_list_old = line_list
            line_list = [[line[0], line[7]]]  # присваиваем свое значение
            _date_old = _date
    return payment


if __name__ == '__main__':
    start = perf_counter()
    block = WF.read_files_block('C:\\report', '.txt')

    #for x in block:
    #    print(x[0])
    end = perf_counter()  # получение времени
    print(end - start)  # расчет времени

    # block, company_dict, payment_doc = read_files_block('C:\\report', '.txt')
    # print('---------------------------------------------------------------------------------------')
    # test.test_list_date(block, '08.06.2021') # тестирование для вывода данных по дате
    # print('---------------------------------------------------------------------------------------')
    # block_s = sort_block(block)
    # payment_doc = processing(sort_block(block))
    # payment_list(block, payment_doc)
    # end = perf_counter()  # получение времени
    # print(end - start)  # расчет времени
# print(test.test_data(block_s, '2016.09.01', '2016.10.10'))
