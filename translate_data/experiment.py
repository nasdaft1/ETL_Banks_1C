# -*- coding:utf8 -*-
import dict_list_company as dt
import line_data as ld

_cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
         "НазначениеПлатежа="]

a = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12', 'a13', 'a14', ]
s1 ='2020,01.01'
#s1 ='01,01.2020'
print(s1.find('.'))

# print(dir(ld.LineData))
f = ld.LineData()
print(1)
setattr(f, 'payer_inn', 'dd')
print(2)
print(f)
print(3)
print('распечатывается')
f.summa = '1.6'
f.date = '01.01.2020'
f.date = '2021.01.01'
f.number = '99'
f.summa = '2021.0350'
#setattr(f, 'payer_name', 'dd')
# setattr(f,'payer_inn','ddd')
print(f)
print(f)
print(f)
print(f)
print(f.__dict__)
print(f.__dict__)
print(f.__dict__)


print(dt.cell[1][0])
#f.clear()
#print(f.__dict__)
