# -*- coding:utf8 -*-
import os
import processing as PR


def find_file(path, exp_file):  # поиск файлов по дереву каталогов
    find_files_list = []
    for root, dirs, files in os.walk(path):
        find_files_list += [os.path.join(root, name) for name in files if name.find(exp_file) != -1]
    return find_files_list


def read_files_block(_path: str, _file: str):  # 'C:\\report\', '.txt'
    # ищем файлы в каталоге [path] с расширением [*.txt]
    block = []  # список транзакции по счетам
    company_dict = {}  # список компаний
    # payment_doc = {}  # список ?????
    for path_file in find_file(_path, _file):
        print('обрабатываем фаил ' + path_file)
        # получаем из файла список транзакции и словарь названия компании +ИНН
        block_x, company_dict = PR.С1_reading_file(path_file, company_dict)
        block += block_x  # собираем полный список транзакции из всех файлов
    return block


def write_file(path_file: str, block: list):  # запись списка в фаил
    file = open(path_file, 'w')
    for line_block in block:
        new_line = map(lambda x: str(x) + '\t', line_block)
        file.writelines(new_line)
        file.write('\n')
    file.close()
