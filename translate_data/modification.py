
def visual(block: list):
    for x in block:
        if x.owner == 'B3' or x.owner == 'K3':
            print(f'\033[31m{x}\033[0m')
        elif x.owner == 'B2' or x.owner == 'K2':
            print(f'\033[32m{x}\033[0m')
        elif x.owner == 'B1' or x.owner == 'K1':
            print(f'\033[33m{x}\033[0m')
        elif x.netting is True:
            print(f'\033[34m{x}\033[0m')
        elif x.cash is True:
            print(f'\033[35m{x}\033[0m')
        else:
            print(x)








def modific_data_fields(block_old:list)-> list:
    block = sorted(block_old, key=lambda x: x.date)  # сортировка списака по дате транзакций
    for index in range(len(block)):
        owner = block[index].owner
        x =True
        if owner == 'B3' or owner == 'K3':
            block[index].owner =owner[0]
            block[index].tax =True
            print(f'\033[31m{block[index]}\033[0m')
            x =False

        if owner == 'B2' or owner == 'K2':
            block[index].owner =owner[0]
            block[index].tax =True
            print(f'\033[31m{block[index]}\033[0m')
            x =False

        if block[index].recipient_name is not None:
            if block[index].recipient_name.find('УФК')!=-1:
                block[index].tax =True
                print(f'\033[32m{block[index]}\033[0m')
                x = False

        if block[index].cash_register is True:
            print(f'\033[34m{block[index]}\033[0m')
            x = False

        if block[index].payment_purpose is not None:
            if block[index].payment_purpose.find('Возмещение средств по операциям') != -1 or \
                    block[index].payment_purpose.find('Возврат по операции с п/к') != -1:
                    #block[index].payment_purpose.find('Комиссия по реестру') != -1 or \

                block[index].cash = False
                block[index].cash_register = True
                print(f'\033[33m{block[index]}\033[0m')
                x = False

        if x is True:
            print(block[index])
    #visual(sorted_list)
    return block
