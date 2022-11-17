# -*- coding:utf8 -*-
from time import perf_counter
import test
import configparser
import work_file as wf
import processing as pr
import compensation as cm
import tax_compensation as tc
import modification as mo
import calculations as calc
import xlsx


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
    # test.test_owner(block)
    block = cm.compensation(block)
    # test.test_owner(block) # получить список названи владельцев опреций и их количество
    # test.test_visual_None(block)
    # test.test_visual(block, 'K1')
    # test.test_visual(block, 'B2')

    print('----------------------------------------------------------------------')
    # test.test_data_summ1(block)
    # test.test_data_summ(block, '2020.01.01', '2020.12.31')
    # test.test_data_quarter_summ(block)
    # wf.write_file('C:/report/text.csv', block) # запись в файл
    # test.test_data_summ(block, '2020.01.01', '2021.12.31', 'B2') получить сисок операций с набегающей суммов на конкретного владельца операции
    tc.data_quarter_summ(block)  # расчет пропорций оплат налогов субъектами
    block = mo.modific_data_fields(block)
    print('-------------------------------------------------------------------------------------------------------')
    test.test_owner(block)  # получить список названи владельцев опреций и их количество
    print(perf_counter() - start_time)  # расчет времени
    start_time = perf_counter()
    xt = xlsx.Xlsx('c:\\report\\text.xlsx', block)
    print(perf_counter() - start_time)  # расчет времени
    # calc.summ_quarter(block)
    # calc.summ_bank_account(block)
    # calc.summ_cash_register_quarter(block)
    #wf.write_file('c:\\report\\text.csv', block)

    # wf.write_file_xlsx('c:\\report\\text.xlsx', block)

    # test.test_data_quarter_summ(block)
    # test.test_owner(block)  # подсчет значений обработанных и не обработанных
    #  block = cm.compensation(block)
    # test.test_data_summ(block, '2016.01.01', '2016.12.31')
    # test.com(block)
    # print(block.__sizeof__())
    # pr.payment_bank(block)  # платежи в банк раскивывает хозяйствующим субъектам, которым принадлежат
    # block_m = cm.compensation(block)
    # test.test_find(block, 'Дата=', '2021.09.03', False)
    # test.test_find(block, 'НазначениеПлатежа=', 'Алименты', True)
    # test.test_find(block, 'НазначениеПлатежа=', 'Плата за прием и обработку платежных документов', False)
    # test.test_find(block, 'Владелец=', 'V', False)
    # test.test_find(block, 'Дата=', '2019.09.10', False)
    # test.test_find(block, 'Дата=', '2021.09.03', False)
    # test.test_find(block, 'НазначениеПлатежа=', 'Алименты', True)
    # test.test_find(block, 'НазначениеПлатежа=', 'Плата за прием и обработку платежных документов', False)
