import csv
import time
import asyncio
import configparser
from telethon import TelegramClient
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest


async def setup_telegram_client():
    config = configparser.RawConfigParser()
    config.read('config.ini')

    try:
        API_ID = config['account']['api_id']
        API_HASH = config['account']['api_hash']
        PHONE = config['account']['phone']
        client =  TelegramClient('ss', API_ID, API_HASH)
    except KeyError:
        print("\033[91m[!] run \033[92mpython3 setup.py \033[91mfirst !!\n")
        return None
    
    await client.start()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        client.sign_in(PHONE, input("Введите проверочный код: ", password=input("Введите пароль для подверждение: ")))

    return client


async def get_megagroups(client):
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    return groups


def choose_group(groups):
    print('\033[1;32m Выберите группу для получения участников:')
    for i, g in enumerate(groups):
        print(f'{i}. {g.title}')
    print('')
    g_index = input("Введите номер группы\n>>> ")
    return groups[int(g_index)]


async def scrape_members(client, target_group):
    all_participants = client.iter_participants(target_group)

    print('\nСохранение в файл ...')
    time.sleep(1)
    with open(f"source/{target_group.title}.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash',
                        'name', 'group', 'group id'])
        async for user in all_participants:
            username = user.username or ""
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash,
                            name, target_group.title, target_group.id])

    print(f'Участники успешно собраны в файл {target_group.title}!!')


async def main():
    # Функция для инициализации и подключения к Telegram.
    client = await setup_telegram_client()
    if not client:
        return

    # Функция для получения списка мегагрупп из Telegram.
    groups = await get_megagroups(client)
    # Функция для выбора группы для сбора участников.
    target_group = choose_group(groups)
    # Функция для сбора участников выбранной группы и сохранения их в CSV файл.
    await scrape_members(client, target_group)


if __name__ == "__main__":
    asyncio.run(main())
