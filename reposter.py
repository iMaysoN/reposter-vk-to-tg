import logging
import os
import sys
import vk_api
import telegram
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# VK BOT
vk_token = os.environ['VK_TOKEN']
vk_login = os.environ['VK_LOGIN']
vk_pass = os.environ['VK_PASSWORD']
group_name = 'all_rpg_news'
post_count = 10
vk_session = vk_api.VkApi(login=vk_login, password=vk_pass, token=vk_token)
vk_session.auth(token_only=True)
vk_bot = vk_session.get_api()

# TG BOT
tg_token = os.environ['TELEGRAM_TOKEN']
tg_group_id_for_repost = '@VipTestBotGroup'
tg_bot = telegram.Bot(tg_token)
tg_hook = telegram

# System
last_id_filepath = os.path.join(sys.path[0], 'lastid')
sleep_time_second = os.environ['REPOST_SLEEP_TIME_SEC'] # time between reposts


def get_last_id():
    last_id_file = open(last_id_filepath, 'r')
    last_id = last_id_file.read()
    last_id_file.close()
    return int(last_id)


def write_new_last_id(new_id):
    last_id_file = open(last_id_filepath, 'w')
    last_id_file.write(str(new_id))
    last_id_file.close()


def main():
    response = vk_bot.wall.get(domain=group_name, count=post_count)
    response = reversed(response['items'])
    for post in response:
        post_id = int(post['id'])
        last_id = get_last_id()
        if last_id >= post_id:
            continue

        owner_id = post['owner_id']
        repost_url = 'https://vk.com/{0}?w=wall{1}_{2}'.format(group_name, owner_id, post_id)
        tg_bot.send_message(chat_id=tg_group_id_for_repost, text=repost_url)
        write_new_last_id(post_id)
        time.sleep(sleep_time_second)


# repost from vk to telegram
if __name__ == '__main__':
    main()
