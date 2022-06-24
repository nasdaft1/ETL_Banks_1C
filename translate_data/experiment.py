# -*- coding:utf8 -*-
import dict_company

_cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
         "НазначениеПлатежа="]
_cell_mod = []
x = {"2": 2}
_cell_mod.append(x.copy())
x = {"2": 1}
_cell_mod.append(x.copy())
x = {"2": 10}
_cell_mod.append(x.copy())
_cell_mod.append(x.copy())
_cell_mod.append(x.copy())
x.clear()
x = {"2": 11}
print(_cell_mod)

d = dict_company.dict_company2.copy()
d.pop('ООО "ИНТЕРКОМ"')
print(d)
