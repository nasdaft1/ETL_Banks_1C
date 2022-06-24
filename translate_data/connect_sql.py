# -*- coding:utf8 -*-
import pyodbc as db  # подключение модуля для БД MSSQL


def test_con():
    sql_driver = 'SQL Server'  # название драйвера посмотреть BDE ADMINISTRATOR ODBC
    sql_server_ip = '192.168.1.202'  # адрес расположение сервера MSSQL
    sql_server_port = '1433'  # порт для подключения
    sql_server_name = 'MSSQL2019'  # имя сервера MSSQL
    sql_db = 'Test1'  # база данных к которой подключаемся
    sql_user = ''  # логин для подлючения к серверу MSSQL
    sql_password = ''  # пароль для подлючения к серверу MSSQL
    try:
        # не забывайте удалать пробелы возле = иначе возникают ошибки
        connectionString = (f'DRIVER={{{sql_driver}}};'
                            f'HOST={sql_server_ip};PORT={sql_server_port};'
                            f'SERVER=.\{sql_server_name};DATABASE={sql_db};')

        if (sql_user == '') and (sql_password == ''):
            connectionString += 'Trusted_Connection=yes;'
        else:
            connectionString += f'UID={sql_user};PWD={sql_password};'
        con = db.connect(connectionString)
        cur = con.cursor()
        requestString = """INSERT INTO Table_1(productid, productname, unitprice) VALUES (10,'fff',2.4) """
        print(requestString)
        cur.execute(requestString)
        cur.commit()
        print("Подключение произведено " + connectionString)
    finally:
        print("Подключение произведено " + connectionString)
        cur.close()  # закрытие курсора
        con.close()  # закрытие подключения к базе данных
