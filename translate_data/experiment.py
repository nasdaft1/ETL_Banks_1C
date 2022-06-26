# -*- coding:utf8 -*-
import dict_list_company as dt

_cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
         "НазначениеПлатежа="]


value = None
r_value = dt.dict_company_name.setdefault('ООО "Интерком"', value)
print(r_value)
r_value = dt.dict_company_name.setdefault('ПАО "МТС"', value)
print(r_value)