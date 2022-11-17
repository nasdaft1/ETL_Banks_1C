# -*- coding:utf8 -*-
import os


def _cell_mod() -> list:  # функция для получения длины слов, для ускорения выполнения программы и упрощения модицикации кода
    _cell = ["Плательщик1=", "Получатель1=", "ПлательщикИНН=", "ПолучательИНН=", "Номер=", "Сумма=", "Дата=",
             "НазначениеПлатежа="]
    _cell_complement = []
    for name in _cell:
        _cell_complement.append([name, len(name)])
    return _cell_complement


def С1_reading_file(path_and_file: str, company_dict: dict):  # чтение файлов 1С формата выгрузки с банка
    _block = []  # список транзакции по счетам
    _line = {}  # создать словарь по транзакции
    _cell = _cell_mod()  # получение словаря данных по которым будет произодится поиск данных

    file2 = open(path_and_file, mode='r')
    for read_line in file2:
        line_modified = read_line.rstrip('\n')  # удалить enter перенос строки
        for name in _cell:  # перебор обрабатывемых полей
            if line_modified.find(name[0]) == 0:  # найти необходимое поле
                _line[name[0]] = line_modified[name[1]:]  # добавления данных в словарь

        if line_modified.find("КонецДокумента") == 0:  # окончание транзакции
            # необходимо создать копию объекта в противном случае все данные стираются clear
            _block.append([_line.copy()])
            # company_dict[_line.setdefault("ПлательщикИНН=", None)] = _line.setdefault("Плательщик1=", None)
            # company_dict[_line.setdefault("ПолучательИНН=", None)] = _line.setdefault("Получатель1=", None)
            company_dict[_line.setdefault("Плательщик1=", None)] = _line.setdefault("ПлательщикИНН=", None)
            company_dict[_line.setdefault("Получатель1=", None)] = _line.setdefault("ПолучательИНН=", None)

            _line.clear()
    file2.close()
    return company_dict


def write_file(path_file: str, block: list):  # запись списка в фаил
    file = open(path_file, 'w')
    for line_block in block:
        new_line = map(lambda x: str(x) + '\t', line_block)
        # print(line_block)
        file.writelines(new_line)
        file.write('\n')
    file.close()


def find_file(path, exp_file) -> list:  # поиск файлов по дереву каталогов
    find_files_list = []
    for root, dirs, files in os.walk(path):
        find_files_list += [os.path.join(root, name) for name in files if name.find(exp_file) != -1]
    return find_files_list


def read_files_block(_path: str, _file: str) -> dict:  # 'C:\\report\', '.txt'
    # ищем файлы в каталоге [path] с расширением [*.txt]
    company_dict = {}  # список компаний
    for path_file in find_file(_path, _file):
        print('обрабатываем фаил ' + path_file)
        # получаем из файла список транзакции и словарь названия компании +ИНН
        company_dict = С1_reading_file(path_file, company_dict)
    return company_dict

# company_dict= read_files_block('C:\\report', '.txt')
# for x,y in company_dict.items():
#     print(x,y)
#     d = dict_company.dict_company2.copy()
#     d1 = dict_company.dict_company2.copy()
#     for x, y in dict_company.dict_company.items():
#         for x1, y1 in d.items():
#             if x == y1:
#                # print(x1,x,y1)
#                 d1.pop(x1)
#     d2 = dict_company_old.dict_company
#     for x, y in d1.items():
#         print("'"+x+"':'"+d2[x]+"',")
