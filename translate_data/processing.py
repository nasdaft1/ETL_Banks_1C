# -*- coding:utf8 -*-
import dict_list_company as dt


#def test(v1, v2, v3, v4, v5, v6, v7):
#    l = [v1, v2, v3, v4, v5, v6, v7]
#    for x in range(2,7):
#        if l[x-1]!='X' and l[x]=='X':
#            return 'error'
#    return 'ok'


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
    for line in dt.list_date_payments_exception:
        if line[1] == '<':
            if date < line[0] and payment_purpose.find(line[2]) != -1:
                value = line[3]
        if line[1] == '>':
            if date > line[0] and payment_purpose.find(line[2]) != -1:
                value = line[3]
    return value


def owner(_line_dict):  # распределение кто является владельцем данного платежа
    value = 'X'
    # определение кому из хозяиствующих субъектов принадлежит счет, исключений
    _payer_name_inn = _line_dict.setdefault("ПлательщикИНН=")  # для dict_company
    _recipient_name_inn = _line_dict.setdefault("ПолучательИНН=")  # для dict_company
    value1 = owner_inn(_payer_name_inn, value)
    value2 = owner_inn(_recipient_name_inn, value1)

    _payer_name = _line_dict.setdefault("Плательщик1=")  # для dict_company_not_inn
    _recipient_name = _line_dict.setdefault("Получатель1=")  # для dict_company_not_inn

    value3 = owner_name(_payer_name, value2)
    value4 = owner_name(_recipient_name, value3)

    _number = _line_dict.setdefault("Номер=")  # для dict_company_exception
    _date = _line_dict.setdefault("Дата=")  # для dict_company_exception
    _payment_purpose = _line_dict.setdefault("НазначениеПлатежа=")  # для dict_company_exception
    value5 = owner_date_payments(_date, _payment_purpose, value4)  # исключение по дате и названию платежки
    value6 = owner_exceptions_purpose(_payment_purpose, value5)
    value7 = owner_exceptions_number_date(_number, _date, value6)
    # if  _payer_name_inn =='6321327104' or '6321327104'==_recipient_name_inn:
    #if test(value1, value2, value3, value4, value5, value6, value7)=='error':
    #    print(value1, value2, value3, value4, value5, value6, value7, _payment_purpose)
    #    print('             ', _payer_name, _recipient_name, _payer_name_inn, _recipient_name_inn)
    return value7


def _cell_mod():  # функция для получения длины слов, для ускорения выполнения программы и упрощения модицикации кода
    _cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
             "НазначениеПлатежа="]
    _cell_complement = []
    for name in _cell:
        _cell_complement.append([name, len(name)])
    return _cell_complement


def reading_file_KC(path_and_file: str):  # чтение файлов 1С формата выгрузки с банка
    file1 = open(path_and_file, mode='r')  # для ускорения кода произодится однократный поиск КС банка
    n = 0
    for read_line_start in file1:
        n += 1
        if n == 20:  # для уменьшение поиска значения увеличение производительности если фаил не корректный
            _settlement_bank = ''
            break  # прервать если в начале файла не найдены нужные файлы
        if read_line_start.find("РасчСчет=") == 0:
            _settlement_bank = read_line_start[len("РасчСчет="):]
            break  # при находжение необходимой строки с данными производится прерывание чтения файла
    file1.close()  # закрываем фаил
    return _settlement_bank[:-1]


def summ_convert(_line, txt):
    """
    :param _line: словарь
    :param txt: название ключа котрое обрабатываем
    :return: словарь в котором меняем тип данных на float по указанному ключу txt
    """
    _summa = _line.setdefault(txt, None)
    if _summa != None:  # переделывает тип в float
        try:
            _line[txt] = float(_summa)
        except:
            _line[txt] = str(_summa)
    return _line


def date_convert(_line, txt):  # переделывает формат в нормальную дату
    """
    :param _line: словарь со значениями
    :param txt: название поле с датой  - type(str)
    преобразует дату ДД.MM.ГГГГ в ГГГГ.ММ.ДД
    :return:  год.месяц.день  - type(str)
    """
    _date = _line.setdefault(txt, None)
    if _date != None:
        _line[txt] = _date[6:] + '.' + _date[3:5] + '.' + _date[0:2]
    return _line


def status(_line):  # определение типа операции по ИНН Плательшика debit/credit
    if _line.setdefault("ПлательщикИНН=", None) == '6324030091':
        #    _owner = owner(_recipient_name, _date_correct, _number, _payment_purpose)
        _line["Статус="] = 'Credit'
    else:
        #    _owner = owner(_payer_name, _date_correct, _number, _payment_purpose)
        _line["Статус="] = 'Debit'
    return _line


def С1_reading_file(path_and_file: str, company_dict: dict):  # чтение файлов 1С формата выгрузки с банка
    _block = []  # список транзакции по счетам
    _line = {}  # создать словарь по транзакции
    _cell = _cell_mod()  # получение словаря данных по которым будет произодится поиск данных
    _settlement_bank = reading_file_KC(
        path_and_file)  # получение кор счета(КС) банка с которого произведена выгрузка данных

    file2 = open(path_and_file, mode='r')
    for read_line in file2:
        line_modified = read_line.rstrip('\n')  # удалить enter перенос строки
        for name in _cell:  # перебор обрабатывемых полей
            if line_modified.find(name[0]) == 0:  # найти необходимое поле
                _line[name[0]] = line_modified[name[1]:]  # добавления данных в словарь

        if line_modified.find("КонецДокумента") == 0:  # окончание транзакции
            _line["КС="] = _settlement_bank
            summ_convert(_line, "Сумма=")
            date_convert(_line, "Дата=")
            status(_line)
            value = owner(_line)
            _line['Владелец='] = value
            # необходимо создать копию объекта в противном случае все данные стираются clear
            _block.append([_line.copy()])
            # company_dict[_line.setdefault("ПлательщикИНН=", None)] = _line.setdefault("Плательщик1=", None)
            # company_dict[_line.setdefault("ПолучательИНН=", None)] = _line.setdefault("Получатель1=", None)
            # company_dict[_line.setdefault("Плательщик1=", None)] = _line.setdefault("ПлательщикИНН=", None)
            # company_dict[_line.setdefault("Получатель1=", None)] = _line.setdefault("ПолучательИНН=", None)
            _line.clear()
    file2.close()
    return _block, company_dict
