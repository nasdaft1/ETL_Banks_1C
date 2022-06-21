# -*- coding:utf8 -*-
import os
from time import perf_counter
import dict_company as dt
import test
import pyodbc as db  # подключение модуля для БД MSSQL


def owner(key, _date, _number, _payment_purpose):
    value = dt.dict_company.setdefault(key, 'N')
    # определение кому из хозяиствующих субъектов принадлежит счет, исключений
    if 'Алименты' in _payment_purpose:
        if _date < '2017.04.15':
            value = 'B'
        else:
            value = 'K'
    if 'бухгалтерские' in _payment_purpose:
        if _date < '2020.02.01':
            value = 'B'
    if 'Возврат по операции' in _payment_purpose:
        value = 'B'
    if 'Заявка на внесение наличных' in _payment_purpose:
        value = 'B'
    if 'Комиссия за ведение банковского' in _payment_purpose:
        value = 'B'
    if 'за терминал' in _payment_purpose:
        value = 'B'
    if 'депозит' in _payment_purpose:
        value = 'B'
    if 'процентов' in _payment_purpose:
        value = 'B'
    if 'Страховые взносы' in _payment_purpose:
        value = 'B'
    if 'страховые взносы' in _payment_purpose:
        value = 'B'
    if 'Возмещение средств по операциям' in _payment_purpose:
        value = 'B'
    if 'Комиссия по реестру' in _payment_purpose:
        value = 'B'
    if 'Налог на доходы физических лиц' in _payment_purpose:
        value = 'B'
    if 'временная финансовая помощь' in _payment_purpose:
        value = 'B'
    if 'Комиссия за открытие счета' in _payment_purpose:
        value = 'B'
    if 'подлинности подписей' in _payment_purpose:
        value = 'B'
    if 'Налог, уплачиваемый при применении УСН' in _payment_purpose:
        value = 'X'
    if _number == '140' and _date == '2021.08.12':  # одноразовая покупка КВАНТ
        value = 'B'
    if _number == '1' and _date == '2015.04.14':  # Возврат по ПП No 1 от 07/04/2015
        value = 'B'
    if _number == '268576' and _date == '2016.09.06':  # ЛАСКИНА ЕЛЕНА АНАТОЛЬЕВНА
        value = 'K'
    if _number == '17' and _date == '2019.01.31':  # одноразовая покупка КОМПАСС
        value = 'B'
    if _number == '102' and _date == '2021.06.08':  # одноразовая покупка КОМПАСС
        value = 'B'
    if _number == '45' and _date == '2017.05.11':  # одноразовая покупка КОМПАСС
        value = 'B'
    if _number == '65' and _date == '2016.06.14':  # одноразовая покупка КОМПАСС
        value = 'B'
    if _number == '194' and _date == '2019.11.14':  # одноразовая покупка ВсеИнструменты
        value = 'B'
    if _number == '15' and _date == '2020.01.28':  # одноразовая покупка ВсеИнструменты
        value = 'K'
    if _number == '103' and _date == '2020.06.03':  # одноразовая покупка ВсеИнструменты
        value = 'K'
    if _number == '155' and _date == '2019.09.26':  # одноразовая покупка ВсеИнструменты
        value = 'K'
    if _number == '15' and _date == '2020.01.27':  # одноразовая покупка ВсеИнструменты
        value = 'K'
    if _number == '121' and _date == '2016.10.03':  # оплата за платеж прошла через несколько дат
        value = 'K'
    if _number == '980' and _date == '2019.05.20':  # на основании ст.46 НК РФ
        value = 'B'
    return value


def find_str(path_str: str, full_str: str, old_value: str, reset_str: str):
    if full_str.find(reset_str) == 0:
        return ''  # при новой секции значения переменной сбрасываются
    if full_str.find(path_str) == 0:
        _value = full_str[len(path_str):]
        return _value  # при нахождении нужного фрагмента текста значение после него присваивается return функции
    return old_value  # выводит старое значение функции без изменения


def find_str_doc(path_str: str, full_str: str, old_value: str):
    return find_str(path_str, full_str, old_value, "СекцияДокумент=")


def find_str_bank(path_str: str, full_str: str, old_value: str):
    return find_str(path_str, full_str, old_value, "КонецФайла")


def С1_reading_file(path_and_file: str, company_dict: dict):  # чтение файлов 1С формата выгрузки с банка
    _block = []  # список транзакции по счетам
    _settlement_bank, _status, _owner, _payer, _recipient, _payer_name, _recipient_name, _date, _number, _summa, _payment_purpose \
        = '', '', '', '', '', '', '', '', '', '', ''
    for read_line in open(path_and_file, mode='r'):
        line_modified = read_line.rstrip('\n')  # удалить enter перенос строки
        _settlement_bank = find_str_bank("РасчСчет=", line_modified,
                                         _settlement_bank)  # расчетный счет по которому проводятся операции
        _payer_name = find_str_doc("Плательщик1=", line_modified, _payer_name)  # имя плательщика операции
        _recipient_name = find_str_doc("Получатель1=", line_modified, _recipient_name)  # имя получателя операции
        _payer = find_str_doc("ПлательщикИНН=", line_modified, _payer)  # ИНН плательщика операции
        _recipient = find_str_doc("ПолучательИНН=", line_modified, _recipient)  # ИНН получателя операции
        _date = find_str_doc("Дата=", line_modified, _date)  # дата операции
        _number = find_str_doc("Номер=", line_modified, _number)  # номер операции
        _summa = find_str_doc("Сумма=", line_modified, _summa)  # cумма операции
        _payment_purpose = find_str_doc("НазначениеПлатежа=", line_modified, _payment_purpose)  # назначение платежа

        _date_correct = _date[6:] + '.' + _date[3:5] + '.' + _date[0:2]  # переделывает формат в нормальную дату
        _settlement_bank
        if line_modified.find("КонецДокумента") != -1:  # создание списков на основе переменных
            if _payer == '6324030091':
                _owner = owner(_recipient_name, _date_correct, _number, _payment_purpose)
                _status = 'Credit'
            else:
                _owner = owner(_payer_name, _date_correct, _number, _payment_purpose)
                _status = 'Debit'
            _block.append(
                # можно только добавлять новые переменные но не менять местами это нарушит код остальных функции
                [_owner, _status, _payer, _recipient, _payer_name, _recipient_name,
                 _date_correct, _number, _summa,
                 _payment_purpose, _settlement_bank, 'external'])
            # для составления словаря контрагентов с которыми работают менеджеры
            company_dict[_recipient_name] = _recipient  # добавить в словарь получателя
            company_dict[_payer_name] = _payer  # добавть в словарь плательщика
    return _block, company_dict


def find_file(path, exp_file):  # поиск файлов по дереву каталогов
    find_files_list = []
    for root, dirs, files in os.walk(path):
        find_files_list += [os.path.join(root, name) for name in files if name.find(exp_file) != -1]
    return find_files_list


def read_files_block(_path: str, _file: str):  # 'C:\\report\', '.txt'
    # ищем файлы в каталоге [path] с расширением [*.txt]
    block = []  # список транзакции по счетам
    company_dict = {}  # список компаний
    payment_doc = {}  # список ?????
    for path_file in find_file(_path, _file):
        print('обрабатываем фаил ' + path_file)
        # получаем из файла список транзакции и словарь названия компании +ИНН
        block_x, company_dict = С1_reading_file(path_file, company_dict)
        block += block_x  # собираем полный список транзакции из всех файлов
    return block, company_dict, payment_doc


def write_file(path_file: str, date: list):  # запись списка в фаил
    file = open(path_file, 'w')
    for line_block in block:
        new_line = map(lambda x: x + '\t', line_block)
        # print(line_block)
        file.writelines(new_line)
        file.write('\n')
    file.close()


def find_x(_owner: str, _number: str, _correction_list: list):
    if _owner == 'X':  # определяем не распределенные платежки банку за обслуживание платежей
        for position_x in _correction_list:
            if (position_x[1] == _number and position_x[0] != 'X'):
                return position_x[0]
    return _owner


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
        if line[0] == 'O':
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
            #Составление словаря с контрагентами неизвестно кому пренадлежацими
            n += 1
            company_dict_N[line[4]] = 'N'
            company_dict_N[line[5]] = 'N'

    for key, value in company_dict_N.items():
        # распечатывание словаря с контрагентами неизвестно кому пренадлежацими
        print("'"+key + "':'" + value+"',")
    print(' Налоги X=', x, '\n Хозяйствующий субъект K=', k,
          '\n Хозяйствующий субъект B=', b, '\n Совместное использование O=', o, '\n Неизвестный хоз. субъект N=', n)


def sort_block(block: list):
    return sorted(block, key=lambda block: block[6])  # производим сортировку по полю дата в много мерном списке


def processing(block: list):
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


def test_con():
    sql_driver = 'SQL Server'  # название драйвера посмотреть BDE ADMINISTRATOR ODBC
    sql_server_ip = '192.168.1.202'  # адрес расположение сервера MSSQL
    sql_server_port = '1433'  # порт для подключения
    sql_server_name = 'MSSQL2019'  # имя сервера MSSQL
    sql_db = 'Test1'  # база данных к которой подключаемся
    sql_user = ''  # логин для подлючения к серверу MSSQL
    sql_password = ''  # пароль для подлючения к серверу MSSQL
    try:
        # не забывайте удалать пробелы возле = иначе возникают ошибки
        connectionString = (f'DRIVER={{{sql_driver}}};'
                            f'HOST={sql_server_ip};PORT={sql_server_port};'
                            f'SERVER=.\{sql_server_name};DATABASE={sql_db};')

        if (sql_user == '') and (sql_password == ''):
            connectionString += 'Trusted_Connection=yes;'
        else:
            connectionString += f'UID={sql_user};PWD={sql_password};'
        con = db.connect(connectionString)
        cur = con.cursor()
        requestString = """INSERT INTO Table_1(productid, productname, unitprice) VALUES (10,'fff',2.4) """
        print(requestString)
        cur.execute(requestString)
        cur.commit()
        print("Подключение произведено " + connectionString)
    finally:
        print("Подключение произведено " + connectionString)
        cur.close()  # закрытие курсора
        con.close()  # закрытие подключения к базе данных


if __name__ == '__main__':
    test_con()
    start = perf_counter()
    block, company_dict, payment_doc = read_files_block('C:\\report', '.txt')
    # test.test_list(block)

    # test.test_payment_doc(company_dict)
    write_file('C:\\report\\text.csv', block)
    end = perf_counter()  # получение времени
    print(end - start)  # расчет времени
    print('---------------------------------------------------------------------------------------')
    # test.test_list_date(block, '08.06.2021') # тестирование для вывода данных по дате
    # print('---------------------------------------------------------------------------------------')
    block_s = sort_block(block)
    payment_doc = processing(sort_block(block))
    payment_list(block, payment_doc)
    end = perf_counter()  # получение времени
    print(end - start)  # расчет времени
# print(test.test_data(block_s, '2016.09.01', '2016.10.10'))
