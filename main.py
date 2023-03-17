import io

import vk_api
import json
import os
import requests
import aiohttp
import asyncio
import aiogram
from aiogram import types, Dispatcher

from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

load_dotenv()

# Initialize the VKontakte API session using your app's API access token and the group ID
VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN, api_version='5.131')

# Create an instance of the VKontakte API client for groups
vk = vk_session.get_api()
bot = aiogram.Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)


def add_entry(post_id, message_id):
    with open('data.txt', 'a') as f:
        f.write(f'{post_id}:{message_id}')


def process_attachments(elements):
    attachments = []

    for el in elements:
        if el['type'] == 'photo':
            sorted_photos = sorted(el['photo']['sizes'], key=lambda x: x['height'] * x['width'], reverse=True)

            attachments.append(('photo', sorted_photos[0]['url']))
        elif el['type'] == 'video':
            attachments.append(('video', f"https://vk.com/video{el['video']['owner_id']}_{el['video']['id']}"))
        elif el['type'] == 'doc' and el['doc']['ext'] == 'gif':
            video_url = el['doc']['preview']['video']['src']
            attachments.append(('gif', video_url))

    return attachments


def process_text(post, event):
    if 'signer_id' in event:
        post['text'] = f'{post["text"]}\n\n<a href="vk.com/id{event["signer_id"]}">Автор</a>'
    elif post['text'] == '':
        post['text'] = None

    return post


def add_videos(post):
    for el in post['attachments']:
        if el[0] == 'video':
            post['text'] = f'{post["text"]}\n\n{el[1]}'

    post['attachments'] = [el for el in post['attachments'] if el[0] != 'video']
    return post


async def handle_post(event):
    obj = event['object']
    post = {
        'text': obj['text'],
        'attachments': process_attachments(obj['attachments'])
    }

    post = add_videos(post)
    post = process_text(post, obj)

    match len(post['attachments']):
        case 0:
            await send_text_message_to_channel(TELEGRAM_CHANNEL_ID, post)
        case 1:
            await send_photo_to_channel(TELEGRAM_CHANNEL_ID, post)
        case _:
            await send_media_group_to_channel(TELEGRAM_CHANNEL_ID, post)


async def run_script():
    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            await handle_post(event.raw)


async def send_text_message_to_channel(channel_id, post: dict):
    await bot.send_message(chat_id=channel_id, text=post['text'].strip(), parse_mode='HTML')


async def send_photo_to_channel(channel_id, post):
    await bot.send_photo(chat_id=channel_id, photo=post['attachments'][0][1], caption=post['text'].strip(),
                         parse_mode='HTML')


async def send_media_group_to_channel(channel_id, post):
    media = types.MediaGroup()

    for i, el in enumerate(post['attachments']):
        caption = post['text'] if i == 0 else None
        if el[0] == 'photo':
            media.attach_photo(el[1], caption, parse_mode='HTML')
        if el[0] == 'gif':
            media.attach_photo(el[1], caption, parse_mode='HTML')

    await bot.send_media_group(channel_id, media=media)


if __name__ == "__main__":
    asyncio.run(run_script())