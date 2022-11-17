# -*- coding:utf8 -*-
import copy

import dict_list_company as dt

import line_data as ld


def separation(data_line):  # для создания транзакция по взаимных расчетов оплаты общих услуг организации
    owner_res = None
    dl = dt.list_date_owner
    data_line1 = copy.copy(data_line)  # копирование объекта
    data_line2 = copy.copy(data_line)  # копирование объекта
    len_dt = len(dl)
    for x in range(len_dt):
        owner = data_line.owner
        date = data_line.date
        status = bool(data_line.status)  # status is True определяет какие деньги поступали от клиентов на счет
        if (dl[x][0] == owner) and (dl[x][1] < date) and (date < dl[x][2]) and (status is dl[x][7]):
            summa = data_line.summa  # получение суммы для дальнейших расчетов
            summa_a = summa * dl[x][3]  # деление суммы на части согласно пропорции
            owner_res = dl[x][4]  # получение на какого владельца платежки изменить изначальную
            if status is True:  # изменить статус платежки для определения кому пришли деньги
                data_line1.status = not status
            if status is False:  # изменить статус платежки для определения кому пришли деньги
                data_line2.status = not status
            data_line1.netting = True
            data_line2.netting = True
            data_line1.owner = dl[x][5]  # получение на какого владельца платежки изменить согласно list_date_owner
            data_line2.owner = dl[x][6]  # получение на какого владельца платежки изменить согласно list_date_owner
            data_line1.summa = summa_a
            data_line2.summa = summa_a
    return data_line1, data_line2, owner_res


def between_data_line(mutual_set_list: list, status: bool):
    data_line = ld.LineData()
    data_line.date = mutual_set_list[0]
    data_line.payment_purpose = mutual_set_list[1]
    data_line.summa = mutual_set_list[4]  # сумма компенсации
    if status is True:
        data_line.owner = mutual_set_list[3]
        data_line.status = True  # дебит/кредит
    else:
        data_line.owner = mutual_set_list[2]
        data_line.status = False  # дебит/кредит
        data_line.netting = True  # индикатор компенсации
    return data_line


# для создания транзакция по взаимных расчетов между субъектами
def between_themselves(block: list, date_max) -> list:
    mutual_set = dt.mutual_settlements  # получения копию списка транзакций между субъектами
    for line in range(len(block) - 1, 0, -1):
        date_start = block[line].date
        try:
            date_end = block[line + 1].date  # для обработки если добавление после последней транзакции
        except:
            date_end = date_max
        index = 0
        if len(mutual_set) == 0:
            break
        else:
            while 1:
                date = mutual_set[index][0]  # получение даты из списка
                len_mutual = len(mutual_set) - 1
                if (date_start <= date) and (date <= date_end):
                    block.insert(line, between_data_line(mutual_set[index], True))  # добавление данных в таблицу
                    block.insert(line, between_data_line(mutual_set[index], False))  # добавление данных в таблицу
                    # удаляем элемент из списка в противном случае есть вероятность повторного добаления
                    mutual_set.pop(index)
                    if len_mutual == 0:  # для выхода в случае последнего удаления для иск. ошибки
                        break
                    else:
                        index = 0  # для сброса в начальное положение списка mutual_set
                        continue  # для обработки mutual_set если имеют одинаковые даты
                if len_mutual == index:
                    break  # прерывания цикла по достижению конца mutual_set
                index += 1
    return block


# функция для добовления между дат транзакции полученных наличных через кассу
def cash(date_start: str, date_end: str) -> list:
    cash_r = dt.cash_register  # список с транзакциями наличных
    list_data_line = []  # список транзакций
    cash_len = len(cash_r)
    if cash_len == 0:  # если 0 то нет дальнейшего поступления наличных
        return []
    line = 0
    data_line = ld.LineData()
    while cash_len > line:
        date = cash_r[line][0]  # получение даты
        if date_start <= date and date < date_end:
            data_line.date = date
            data_line.owner = 'B'
            data_line.cash = True
            data_line.payment_purpose = cash_r[line][1]
            data_line.cash_register = True
            data_line.status = True

            data_line.summa = cash_r[line][2]
            cash_r.pop(line)
            cash_len -= 1  # при удаление значения из списка уменьшаем его длину
            list_data_line.append(data_line)  # создание списка на добавление транзакций
            continue
        line += 1
    return list_data_line


def compensation(block: list) -> list:
    # модификация данных для компенсации между хозяйствующими субъектами
    # добавление транзакций по перемещению денежных срездст между виртуальными счетами
    # mutual_sett = dt.mutual_settlements  # получения копию списка транзакций между субъектами
    date_max = dt.date_max_processing  # максимальная дата для обработки
    date_end = '2060.01.01'  # максимальная дата до которой возможно будет существовать фирма
    for line in range(len(block) - 1, 0, -1):
        data_line = block[line]
        data_line1, data_line2, owner = separation(data_line)
        if owner is not None:
            data_line.owner = owner
            block.insert(line + 1, data_line1)  # производим вставку в список операций взаиморасчетов x(line_dict)
            block.insert(line + 1, data_line2)  # производим вставку в список операций взаиморасчетов x(line_dict)
        date_start = data_line.date
        # print(date_start, '---', date_end)
        cash_r = cash(date_start, date_end)  # получение список транзакций между датами других транзакций
        for line_cash in range(len(cash_r)):
            block.insert(line, cash_r[line_cash])

        date_end = date_start
    block = between_themselves(block, date_max)

    print(len(block))
    return block
