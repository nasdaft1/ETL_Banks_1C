# -*- coding:utf8 -*-
import os
import processing as pr


width_list = [2, 2, 2, 10, 9, 28, 28, 82, 10, 2, 2, 2, 2, 10]

def find_file(path: str, exp_file: str):  # поиск файлов по дереву каталогов
    find_files_list = []
    for root, dirs, files in os.walk(path):
        find_files_list += [os.path.join(root, name) for name in files if name.find(exp_file) != -1]
    return find_files_list


def read_files_block(_path: str, _file: str):  # 'C:\\report\', '.txt'
    # ищем файлы в каталоге [path] с расширением [*.txt]
    block = []  # список транзакции по счетам
    for path_file in find_file(_path, _file):
        print('обрабатываем фаил ' + path_file)
        # получаем из файла список транзакции и словарь названия компании +ИНН
        block_x = pr.С1_reading_file(path_file)
        block += block_x  # собираем полный список транзакции из всех файлов
    return block


def write_file(path_file: str, block: list):  # запись списка в фаил
    file = open(path_file, 'w')
    for line_x in block:
        # print(line_x)
        if line_x.owner == 'B':

            file.write(str(line_x.number) + '\t')
            file.write(str(line_x.date) + '\t')
            if line_x.status is True:
                file.write(str(line_x.summa) + '\t')
            else:
                file.write(str(-line_x.summa) + '\t')
            file.write(str(line_x.payment_purpose) + '\t')
            file.write(str(line_x.payer_name) + '\t')
            file.write(str(line_x.recipient_name) + '\t')
            # new_line = map(lambda x: str(x) + '\t', line_x)
            # file.writelines(new_line)
            file.write('\n')
    file.close()

