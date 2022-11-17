# -*- coding:utf8 -*-
import dict_list_company as dl


def summ_convert(value):
    """
    :param value: значение в str
    :return: возвращает значение float c двумя заначениями после запятой
    """
    if value is not None:  # переделывает тип в float
        try:
            return_value = round(float(value), 2)
        except ():
            raise NameError(f'Неверный тип данных при преобразовании суммы платежа: {value}')
        return return_value
    else:
        return None


def number_convert(value: str):
    """
    :param value: название ключа котрое обрабатываем
    :return: возвращает значение int
    """
    if value is not None:  # переделывает тип в float
        try:
            return_value = int(value)
        except ():
            raise NameError(f'Неверный тип данных при преобразовании номера платежа: {value}')
        return return_value
    else:
        return None


# не модифицировать
def date_convert(_date):  # переделывает формат в нормальную дату
    """
    :param _date: название поле с датой  - type(str)
    преобразует дату ДД.MM.ГГГГ в ГГГГ.ММ.ДД
    :return:  год.месяц.день  - type(str)
    """
    if _date is not None:
        if (_date[2] == '.') and (_date[5] == '.'):
            return _date[6:] + '.' + _date[3:5] + '.' + _date[0:2]
        elif (_date[4] == '.') and (_date[7] == '.'):
            return _date
        else:
            raise NameError('Неверный тип данных при преобразовании даты')
    else:
        return None


# def cell_mod():  # функция для получения длины слов, для ускорения выполнения программы и упрощения модицикации кода
#    _cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
#             "НазначениеПлатежа=", "РасчСчет="]
#    _cell_complement = []
#    for name in _cell:
#        _cell_complement.append([name, len(name)])
#    return _cell_complement


class Descriptor:

    def __set_name__(self, owner, name):  # Присвоение названия переменной передаваемой в дескриптор = name
        self.name = '_' + name

    def __set__(self, instance, value):  # value значение передаваемое переменной передаваемые в дескриптор
        if self.name == '_date':  # обработка даты в правельный формат
            value = date_convert(value)
        if self.name == '_number':  # преобразование в номера платежки в число
            value = number_convert(value)
        if self.name == '_summa':  # преобразование суммы в тип float с округлением до двух знаков
            value = summ_convert(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, value=None):  # чтение данны содержащихся в дескрипторе
        return instance.__dict__[self.name]


# '6324030091'
class LineData:
    number = Descriptor()  # для обработки передаваемых данны, через дескриптор
    summa = Descriptor()  # для обработки передаваемых данны, через дескриптор
    date = Descriptor()  # для обработки передаваемых данны, через дескриптор

    def __init__(self):
        self.clear()  # создания дефолтных значений через функцию

    def __str__(self):  # для создание формата выгрузки данных на экран
        if self.status is True:
            status = 'Credit'
            summa = self.summa
        elif self.status is False:
            status = 'Debit'
            summa = f'-{self.summa}'
        else:
            status = 'None'
            summa = None

        if self.netting is True:
            netting = 'Взаимозачет'
        elif self.netting is False:
            netting = 'Стандартная оп.'
        else:
            netting = 'None'

        if self.cash is True:
            cash = 'Нал.'
        elif self.cash is False:
            cash = 'Без нал.'
        else:
            cash = 'None'

        if self.tax is True:
            tax = 'Налог.'
        else:
            tax = '-----'

        if self.cash_register is True:
            cash_register = 'Касса'
        else:
            cash_register = '-----  '

        return f'{self.owner},{self.number},{self.date}, {status} ,{summa},{self.payer_inn},' \
               f'{self.payer_name},{self.recipient_inn},{self.recipient_name},{self.payment_purpose},' \
               f'{self.settlement_bank} , {netting},{cash},{tax},{cash_register}:'

    def clear(self):  # очистка значений перевод их в дефолтное значение
        self.payer_inn: str = None  # инн плательщика
        self.recipient_inn: str = None  # инн получателя
        self.payer_name: str = None  # имя плательцика
        self.recipient_name: str = None  # имя получателя
        self.number: int = None  # номер платежа
        self.date: str = None  # дата платежа
        self.summa: float = 0  # сумма платежа
        self.status: bool = None  # статус платежа дебит/кредит
        self.payment_purpose: str = None  # наименование(назначение) платежа
        self.settlement_bank: str = None  # расчетный счет банка осущесчтвляющий операции
        self.owner: str = 'X'  # владелец операции
        self.netting: bool = None  # индикатор операции взаиморасчетов
        self.cash: bool = False  # индикатор операции наличных
        self.tax: bool = False  # индикатор операции налогов
        self.cash_register: bool = False # индикатор операции через кассовый аппарат

