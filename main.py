import eel
from telethon import TelegramClient, events
import asyncio
import datetime

client = None
client2 = None
phone_hash = None
donor_py = None
channel_py = None


async def lg(api_id, api_hash, phone_number):
    global client, phone_hash
    client = TelegramClient('telegram', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        ph = await client.send_code_request(phone_number)
        phone_hash = ph.phone_code_hash
    else:
        return f'Уже авторизованны'
    return f'Смс отправленно, введите его ниже'


async def ec(api_id, api_hash, phone_number, code, donor, channel):
    global client2, phone_hash, donor_py, channel_py
    donor_py = donor
    channel_py = channel
    client2 = TelegramClient('telegram', api_id, api_hash)
    await client2.connect()
    if not await client2.is_user_authorized():
        await client2.sign_in(phone_number, code, phone_code_hash=phone_hash)

    @client2.on(events.NewMessage(chats=(donor)))
    async def normal_handler(event):
        await client2.send_message(channel, event.message)
        eel.prnt(f"{datetime.datetime.now().strftime('%H:%M:%S')} Отправленное сообщение: {event.message.message} <br>")
    await client2.start()
    await client2.run_until_disconnected()


@eel.expose
def login(api_id, api_hash, phone):
    result = asyncio.run(lg(api_id, api_hash, phone))
    return result


@eel.expose
def entry_code(api_id, api_hash, phone, code, donor, channel):
    result = asyncio.run(ec(api_id, api_hash, phone, code, donor, channel))


eel.init("web")
eel.start("main.html", size=(500, 500))
