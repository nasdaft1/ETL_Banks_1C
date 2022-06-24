# -*- coding:utf8 -*-
import dict_company as dt


def owner1(_line_dick):
    _date = _line_dick.setdefault("Дата=")
    _payment_purpose = _line_dick.setdefault("НазначениеПлатежа=")
    _number = _line_dick.setdefault("Номер=")
    # определение кому из хозяиствующих субъектов принадлежит счет, исключений
    _payer_name_inn = _line_dick.setdefault("ПлательщикИНН=")
    _recipient_name_inn = _line_dick.setdefault("ПолучательИНН=")
    _payer_name = _line_dick.setdefault("Плательщик1=")
    _recipient_name = _line_dick.setdefault("Получатель1=")
    if _payer_name_inn == '6324030091':
        # value = 1
        value1 = dt.dict_company.setdefault(_recipient_name_inn, None)
        if value1 is None:
            value1 = dt.dict_company_not_inn.setdefault(_recipient_name, None)
            print(_date, _number, _payment_purpose, _payer_name_inn, _recipient_name_inn, value1)
        else:
            print(_date, _number, _payment_purpose, _payer_name_inn, _recipient_name_inn, value1[1])
    else:
        # value = 2
        value1 = dt.dict_company.setdefault(_payer_name_inn, None)  # _payer_name
        if value1 is None:
            value1 = dt.dict_company_not_inn.setdefault(_recipient_name, None)
            print(_date, _number, _payment_purpose, _payer_name_inn, _recipient_name_inn, value1)
        else:
            print(_date, _number, _payment_purpose, _payer_name_inn, _recipient_name_inn, value1[1])
    # if value1 is None:
    #    print('x')
    # else:
    #    print(_date, _number, _payment_purpose, value, _payer_name_inn, _recipient_name_inn, value1[1])
    #    value1 = dt.dict_company_not_inn.setdefault(_payer_name, 'G')
    #    #value = dt.dict_company.setdefault("ПолучательИНН=", 'N')
    #    value = dt.dict_company.setdefault("ПлательщикИНН=", 'N')
    # else:
    #    value = dt.dict_company.setdefault("ПолучательИНН=", 'N')
    #    #value = dt.dict_company.setdefault("ПлательщикИНН=", 'N')


def owner(_line_dick):
    _date = _line_dick.setdefault('Date=')
    _payment_purpose = _line_dick.setdefault('"НазначениеПлатежа="')
    _number = _line_dick.setdefault('Номер=')
    # определение кому из хозяиствующих субъектов принадлежит счет, исключений
    _payer = _line_dick.setdefault('ПлательщикИНН =')
    print(_date, _payment_purpose, _number, _payer)
    if _payer == '6324030091':
        value = dt.dict_company.setdefault('Получатель1=', 'N')
    else:
        value = dt.dict_company.setdefault('Плательщик1=', 'N')

    if 'Алименты' in _payment_purpose:
        if _date < '2017.04.15':
            value = 'B'
        else:
            value = 'KA'
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
        if n == 20:
            _settlement_bank = ''
            break  # прервать если в начале файла не найдены нужные файлы
        if read_line_start.find("РасчСчет=") == 0:
            _settlement_bank = read_line_start[len("РасчСчет="):]
            break  # при находжение необходимой строки с данными производится прерывание чтения файла
    file1.close()  # закрываем фаил
    return _settlement_bank[:-1]


def summ_convert(_line, txt):
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


def status(_line):  # определение типа операции по ИНН Плательшика
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
            owner1(_line)
            # необходимо создать копию объекта в противном случае все данные стираются clear
            _block.append([_line.copy()])
            # company_dict[_line.setdefault("ПлательщикИНН=", None)] = _line.setdefault("Плательщик1=", None)
            # company_dict[_line.setdefault("ПолучательИНН=", None)] = _line.setdefault("Получатель1=", None)
            company_dict[_line.setdefault("Плательщик1=", None)] = _line.setdefault("ПлательщикИНН=", None)
            company_dict[_line.setdefault("Получатель1=", None)] = _line.setdefault("ПолучательИНН=", None)
            _line.clear()
    file2.close()
    return _block, company_dict
