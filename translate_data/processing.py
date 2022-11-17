# -*- coding:utf8 -*-
import dict_list_company as dt
import line_data as ld


def owner_inn(name_inn, value):  # определение владельца платежа по словарю ИНН компаний
    r_value = dt.dict_company_inn.setdefault(name_inn, None)
    if r_value is None:
        return value
    else:
        return r_value[1]


# def owner_name(name, value):  # определение владельца платежа по словарю название компании или ФИО
#     r_value = dt.dict_company_name.setdefault(name, None)
#     if r_value is None:
#         return value
#     else:
#         return r_value

def owner_name(name, value):  # определение владельца платежа по словарю название компании или ФИО
    for key_dict, value_dict in dt.dict_company_name.items():
        if name.upper().find(key_dict.upper()) != -1: # для поиска частичного совпадения по ключу словаря
            return value_dict
    return value


def owner_exceptions_purpose(payment_purpose, value):
    x_payment = payment_purpose.upper()
    # определение владельца платежа по списку фрагментов названия платежа
    for line in dt.list_payments_exception:
        if x_payment.find(line[0].upper()) != -1:
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


def status(payer_inn, recipient_inn, payment_purpose):  # определение типа операции по ИНН Плательшика debit/credit
    dt.inn_company
    if recipient_inn == '6324030091':  # устанавливаем статус дебит/кредит в зависимости от ИНН
        # для обработки внутренних поличатель и отправитель с одинаковым inn (пример: работа с депозитом)
        if payer_inn == '6324030091':
            for line in dt.list_payments_status:
                if payment_purpose.find(line[0]) != -1:
                    return line[1]
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
            # устанавливаем статус дебит/кредит в зависимости от ИНН
            list_data.status = status(list_data.payer_inn, list_data.recipient_inn, list_data.payment_purpose)
            if (list_data.payer_inn == dt.inn_company) and (list_data.recipient_inn == dt.inn_company):
                list_data.owner = 'B'
            else:
                list_data.owner = owner(list_data)

            _block.append(list_data)  # добавление объекта в список
            list_data = ld.LineData()  # для создания нового объекта с переменными
    file2.close()
    return _block


def payment_bank(block):
    # функция изменения владельца платежа в банк в заваисимости от владельца перевода денег другой организации
    len_block = len(block) - 1  # определение длины обрабатываемых блока
    for line in range(len_block):
        data = block[line]
        bank = data.settlement_bank
        value_owner, value_number = data.owner, data.number
        if value_owner == 'V':  # обрабатываем только Владелец=V
            line_up = line  # определение начальной точки отсчета поиска
            line_down = line  # определение начальной точки отсчета поиска
            n = 0  # для тестирования
            while 1:  # бесконечный цикл пока не сработает break, возможно лучше поставить ограничение для избегание ошибок
                # print(line_up, line_down, len_block)
                if line_up != len_block:  # для исключения ошибок выхода за пределами списка
                    line_up += 1  # счетчик вверх по списку
                if line_down != 0:  # для исключения ошибок выхода за пределами списка
                    line_down -= 1  # счетчик ввниз по списку
                if (line_up == len_block) and (line_down == 0):
                    print(block[len_block])
                    break
                n += 1  # для тестирования
                # Поиск вверх по списке если банк взял комиссию до перевода денег организации
                value_owner_up, value_number_up, bank_up = block[line_up].owner, block[line_up].number, block[
                    line_up].settlement_bank
                # обработка если было насколько платежей организаци в один день != 'V'
                if (value_number_up == value_number) and (value_owner_up != 'V') \
                        and (value_owner_up != 'X') and (bank_up == bank):
                    # присваивается новое значения владельца платежа
                    block[line].owner = value_owner_up
                    break
                # Поиск вниз по списку если банк взял комиссию после перевода денег организации
                value_owner_down, value_number_down, bank_down = \
                    block[line_down].owner, block[line_down].number, block[line_up].settlement_bank
                # обработка если было насколько платежей организаци в один день != 'V'
                if (value_number_down == value_number) and (value_owner_down != 'V') \
                        and (value_owner_down != 'X') and (bank_down == bank):
                    # присваивается новое значения владельца платежа
                    block[line].owner = value_owner_down
                    break
    return block
