# ETL_Banks_1C
Определения:
хозяйствующий субъект организации – это человек в организации, который ведёт одну или несколько хозяйственную  деятельность организации, 
может оперировать единолично или совместно счетами, кассой, сотрудниками.

Техническое задание:
1. Создание ПО для ведения хозяйственной деятельности организации по следующим критериям:
- аренда и суб. аренда
- фотосалон и канцтовары
- монтаж видеонаблюдения
- монтаж охранной сигнализации 
- монтаж системы контроля управления доступа
- техническое обслуживание сигнализации
2. Создание БД на MSSQL или PosgreSQL
3. Создание ПО на Python c web интерфейсом на FLASK
4. ELT файлов 1C.txt в которых ранее велись взаимозачеты между хозяйствующими субъектами.
5. ETL файлов csv из различных банков.
6. В кратчайшие сроки осуществить выше изложенные пункты, упрощая систему но оставляя возможность масштабирования.

Цель:
	- разграничение хозяйственно деятельности на 2 или более частей, которыми оперируют хозяйствующие субъекты.
	- расчет доходов, расходов и ориентировкой налоговой нагрузки по каждому виду деятельность.
	- получение значений эффективности ведения деятельности хозяйствующими субъектами по месяцам.
	-  получение бюджета для хозяйствующих субъектов по сферам деятельности
Особенность:
-	У некоторых контрагентов приобретаются товары или услуги разными хозяйствующими субъектами.
-	Организация имеет 2 в будущем и более расчетными счетами.
-	Некоторые контрагенты иногда оплачивают предоставленные им услуги на расчетный счет другого хозяйствующего субъекта организации.
-	Касса, имеющаяся в фотосалоне, используется всеми хозяйствующими субъектами для ведения своих видов деятельности по оказанию 
услуг физическим лицам, через оплату наличным и безналичном по карте, через терминал.
-	У каждого хозяйствующего субъекта организации имеется свой склад.
-	За период работы организации менялась форма налогообложения, и возможно будет меняться в последующем.

ЭТАПЫ
	1 - Написание программы на Python по сборуданных их файлов различных банков организации.
	2 - Определение кому из хозяйствующих субъектов принадлежат платежи.
	3 - Написание функций в Python для внутренних взаиморасчетов хозяствующ субъетов между собой
	4 - Создание базы данных в MSSQL
	5 - Создание функции загрузки данных в MSSQL
	6 - Выгрузка данных в MSSQL
	

