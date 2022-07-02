# -*- coding:utf8 -*-
from time import perf_counter
import test
import configparser
import work_file as wf
import processing as pr
# import compensation as cm


def sort_block(block: list):
    return sorted(block, key=lambda block: block[6])  # производим сортировку по полю дата в много мерном списке


def start(file_config: str):
    config = configparser.ConfigParser()  # парсинг из конфигурационного файла
    try:
        config.read(file_config, encoding="utf-8")  # открытие файла конфигурации
        try:
            path = config['config']['path']  # путь к каталогу в котором будут искаться фаилы
            file_type = config['config']['file_type']  # тип файлов которые будет искаться
        except KeyError:
            print('\033[1;31mERROR: ошибка конфигурации в файле ' + file_config + ' \033[0m')
    except IOError:
        print('\033[1;31mERROR: ненайден ' + file_config + ' в каталоге \033[0m')
    return wf.read_files_block(path, file_type)


if __name__ == '__main__':
    start_time = perf_counter()
    block = start('config.ini')

    block = pr.payment_bank(block)
    test.test_owner(block)
    test.test_visual(block, 'O')

    # print(block.__sizeof__())
    # pr.payment_bank(block)  # платежи в банк раскивывает хозяйствующим субъектам, которым принадлежат
    # block_m = cm.compensation(block)
    print('-------------------------------------------------------------------------------------------------------')
    # test.test_owner(block)  # подсчет значений обработанных и не обработанных
    #  block = cm.compensation(block)


    end_time = perf_counter()  # получение времени
    print(end_time - start_time)  # расчет времени

    # test.test_find(block, 'Дата=', '2021.09.03', False)
    # test.test_find(block, 'НазначениеПлатежа=', 'Алименты', True)
    # test.test_find(block, 'НазначениеПлатежа=', 'Плата за прием и обработку платежных документов', False)
    # test.test_find(block, 'Владелец=', 'V', False)
    # test.test_find(block, 'Дата=', '2019.09.10', False)
    # test.test_find(block, 'Дата=', '2021.09.03', False)
    # test.test_find(block, 'НазначениеПлатежа=', 'Алименты', True)
    # test.test_find(block, 'НазначениеПлатежа=', 'Плата за прием и обработку платежных документов', False)
