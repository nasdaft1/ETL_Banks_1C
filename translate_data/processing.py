# -*- coding:utf8 -*-
import dict_list_company as dt
import line_data as ld


def owner_inn(name_inn, value):  # определение владельца платежа по словарю ИНН компаний
    r_value = dt.dict_company_inn.setdefault(name_inn, None)
    if r_value is None:
        return value
    else:
        return r_value[1]


def owner_name(name, value):  # определение владельца платежа по словарю название компании или ФИО
    r_value = dt.dict_company_name.setdefault(name, None)
    if r_value is None:
        return value
    else:
        return r_value


def owner_exceptions_purpose(payment_purpose, value):
    # определение владельца платежа по списку фрагментов названия платежа
    for line in dt.list_payments_exception:
        if payment_purpose.find(line[0]) != -1:
            return line[1]
    return value


def owner_exceptions_number_date(number, date, value):
    # определение владельца платежа по номеру и дате платежа как частное исключение из остальных правил
    for line in dt.list_number_date_exception:
        if (line[0] == number) and (line[1] == date):
            return line[2]
    return value


def owner_date_payments(date, payment_purpose, value):
    # определение владельца платежа по дате платежа и фрагменту названия платежа
    for line in dt.list_date_payments_exception:
        if line[1] == '<':
            if date < line[0] and payment_purpose.find(line[2]) != -1:
                value = line[3]
        if line[1] == '>':
            if date > line[0] and payment_purpose.find(line[2]) != -1:
                value = line[3]
    return value


# модифицировать
def owner(arg):  # распределение кто является владельцем данного платежа
    value = 'X'
    value1 = owner_inn(arg.payer_inn, value)
    value2 = owner_inn(arg.recipient_inn, value1)
    value3 = owner_name(arg.payer_name, value2)
    value4 = owner_name(arg.recipient_name, value3)
    value5 = owner_date_payments(arg.date, arg.payment_purpose, value4)  # исключение по дате и названию платежки
    value6 = owner_exceptions_purpose(arg.payment_purpose, value5)
    value7 = owner_exceptions_number_date(arg.number, arg.date, value6)
    return value7


def status(value):  # определение типа операции по ИНН Плательшика debit/credit
    if value == '6324030091':  # устанавливаем статус дебит/кредит в зависимости от ИНН
        return True
    else:
        return False


def С1_reading_file(path_and_file: str):  # чтение файлов 1С формата выгрузки с банка
    _block = []  # список транзакции по счетам
    len_sell = len(dt.cell)  # определение длины списка для последующего организации цикла
    index = 0
    list_data = ld.LineData()
    file2 = open(path_and_file, mode='r')
    for read_line in file2:
        line_modified = read_line.rstrip('\n')  # удалить enter перенос строки
        index += 1  # осуществляется подсчет прочитаных строк из файла
        if index < 20:  # для сняти проверки по всему файлу а только в начале
            if line_modified.find('РасчСчет=') == 0:  # для получение номера счета банка осуществляющего транзакции
                _settlement_bank = line_modified[9:]  # 9 соотвествует длине строки 'РасчСчет='
        for index_sell in range(len_sell):  # перебор обрабатывемых полей
            if line_modified.find(dt.cell[index_sell][0]) == 0:  # найти необходимое поле
                # внесение объект list_data переменных и их значений на основе списка sell
                setattr(list_data, dt.cell[index_sell][1], line_modified[dt.cell[index_sell][2]:])
        if line_modified.find("КонецДокумента") == 0:  # окончание транзакции
            list_data.settlement_bank = _settlement_bank  # определение банка транзитера платежей
            list_data.status = status(list_data.recipient_inn)  # устанавливаем статус дебит/кредит в зависимости от ИНН
            list_data.owner = owner(list_data)
            _block.append(list_data)  # добавление объекта в список
            list_data = ld.LineData()  # для создания нового объекта с переменными
    file2.close()
    return _block


def payment_bank(block):
    # функция изменения владельца платежа в банк в заваисимости от владельца перевода денег другой организации
    for line in range(len(block)):
        data = block[line]

        value_owner, value_number = data.owner, data.number
        if value_owner == 'V':  # обрабатываем только Владелец=V
            line_up = line  # определение начальной точки отсчета поиска
            line_down = line  # определение начальной точки отсчета поиска
            n = 0  # для тестирования
            while 1:  # бесконечный цикл пока не сработает break, возможно лучше поставить ограничение для избегание ошибок
                line_up += 1  # счетчик вверх по списку
                line_down -= 1  # счетчик ввниз по списку
                n += 1  # для тестирования
                # Поиск вверх по списке если банк взял комиссию до перевода денег организации
                value_owner_general_up, value_number_general_up = block[line_up].owner, block[line_up].number
                # обработка если было насколько платежей организаци в один день != 'V'
                if (value_number_general_up == value_number) and (value_owner_general_up != 'V'):
                    # присваивается новое значения владельца платежа
                    block[line].owner = value_owner_general_up
                    break
                # Поиск вниз по списку если банк взял комиссию после перевода денег организации
                value_owner_general_down, value_number_general_down = block[line_down].owner, block[line_down].number
                # обработка если было насколько платежей организаци в один день != 'V'
                if (value_number_general_down == value_number) and (value_owner_general_down != 'V'):
                    # присваивается новое значения владельца платежа
                    block[line].owner = value_owner_general_down
                    break
    return block
