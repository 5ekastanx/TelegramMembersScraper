import os
import configparser

def install_requirements():
    print("Требование к установке ...")
    os.system('python3 -m pip install telethon')
    os.system('pip3 install telethon')

def setup_config():
    cpass = configparser.ConfigParser()
    cpass.add_section('account')

    xid = input("Введите идентификатор API: ")
    cpass.set('account', 'api_id', xid)

    xhash = input("Введите хеш API: ")
    cpass.set('account', 'api_hash', xhash)

    xphone = input("Введите номер телефона: ")
    cpass.set('account', 'phone', xphone)

    with open('config.ini', 'w') as file:
        cpass.write(file)

    print("Настройка завершено!")

def main():
    # Установка необходимых зависимочтей.
    install_requirements()
    # Настройка конфигурацционного файла.
    setup_config()

if __name__ == "__main__":
    main()