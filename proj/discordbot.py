# discordbot.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import django
django.setup()
import discord
import logging
import asyncio
import datetime
from keyword_manager.models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel
from django.db.models import Manager
from asgiref.sync import sync_to_async

class AsyncManager(Manager):
    async def async_all(self, queryset):
        return await sync_to_async(list)(queryset)

logger = logging.getLogger(__name__)


async def loop_message():
    while True:
        now = datetime.datetime.now()
        logging.info(f"{now} for loop_message")
        if now.minute == 10:
            logging.info("send_hotdeal_alerts 실행 시작")
            await bot.send_hotdeal_alerts()
        await asyncio.sleep(60)


class HotdealBot(discord.Client):
    async def on_ready(self):
        logger.info(f'We have logged in as {self.user}')
        await loop_message()
        logging.info("loop_message started")


    async def send_hotdeal_alerts(self):
        # 비동기 쿼리를 실행할 수 있도록 비동기 매니저를 사용
        async_manager = AsyncManager()

        # 활성화된 DiscordMessage 객체들을 가져옴. user와 keyword를 포함해 가져옴.
        active_discord_messages = await async_manager.async_all(
            DiscordMessage.objects.filter(active=True).select_related('user', 'keyword')
        )

        # 유저별로 DiscordMessage 객체를 그룹화
        user_messages = {}  # 빈 딕셔너리를 생성하여 각 유저별로 메시지를 저장할 공간을 만듬
        for discord_message in active_discord_messages:  # 모든 활성화된 DiscordMessage 객체를 순회
            user = discord_message.user  # 각 메시지에서 유저 객체를 가져옴
            if user not in user_messages:  # 유저가 딕셔너리에 없으면
                user_messages[user] = {'discord_uid': discord_message.discord_uid, 'keywords': []}  # 유저를 키로 하고 discord_uid와 키워드 리스트를 값으로 추가
            user_messages[user]['keywords'].append(discord_message.keyword.text)  # 유저의 리스트에 키워드를 추가

        for user, user_data in user_messages.items():  # 그룹화된 유저별 메시지들을 순회
            keywords = user_data['keywords']
            messages = []  # 유저별로 보낼 메시지들을 저장할 리스트

            for keyword in keywords:  # 각 유저의 키워드들을 순회
                # 키워드에 해당하는 핫딜들을 가져옴
                hotdeals = await async_manager.async_all(
                    ScrappingModel.objects.filter(title__icontains=keyword, active=True)
                )
                if hotdeals:  # 핫딜이 있는 경우에만
                    keyword_message = f"'{keyword}' 검색 결과:\n" + "\n".join(
                        [f"{hotdeal.title}: {hotdeal.url}" for hotdeal in hotdeals]
                    )
                    messages.append(keyword_message)  # 메시지 리스트에 추가

            if messages:  # 메시지가 있는 경우에만
                discord_user = await self.fetch_user(user_data['discord_uid'])  # Discord API를 통해 디스코드 유저를 가져옴
                if discord_user:  # 유저가 있는 경우에만
                    # 유저에게 메시지를 보냄
                    await discord_user.send("\n\n".join(messages))
                else:
                    # 유저를 찾을 수 없는 경우 경고 로그를 남김
                    logger.warning(f"Could not fetch Discord user for user ID {user.id}")
            else:
                # 핫딜이 없는 경우 로그를 남김
                logger.info(f"No hot deals found for user {user.username}")



    # async def send_hotdeal_alerts(self):
    #     # 비동기 쿼리를 실행할 수 있도록 비동기 매니저를 사용
    #     async_manager = AsyncManager()

    #     # 활성화된 DiscordMessage 객체들을 가져옴. user와 keyword를 포함해 가져옴.
    #     active_discord_messages = await async_manager.async_all(
    #         DiscordMessage.objects.filter(active=True).select_related('user', 'keyword')
    #     )

    #     # 유저별로 DiscordMessage 객체를 그룹화
    #     user_messages = {}  # 빈 딕셔너리를 생성하여 각 유저별로 메시지를 저장할 공간을 만듬
    #     for discord_message in active_discord_messages:  # 모든 활성화된 DiscordMessage 객체를 순회
    #         user = discord_message.user  # 각 메시지에서 유저 객체를 가져옴
    #         if user not in user_messages:  # 유저가 딕셔너리에 없으면
    #             user_messages[user] = {'discord_uid': discord_message.discord_uid, 'keywords': []}  # 유저를 키로 하고 discord_uid와 키워드 리스트를 값으로 추가
    #         user_messages[user]['keywords'].append(discord_message.keyword.text)  # 유저의 리스트에 키워드를 추가
    #         # {user:{'discord_uid':adfasfasf, 'keywords':['a', 'b', 'c', 'd']}}

    #     for user, user_data in user_messages.items():  # 그룹화된 유저별 메시지들을 순회
    #         keywords = user_data['keywords']
    #         hotdeals = []  # 유저별 핫딜을 저장할 리스트
    #         for keyword in keywords:  # 각 유저의 키워드들을 순회
    #             # 키워드에 해당하는 핫딜들을 가져와서 리스트에 추가
    #             hotdeals.extend(await async_manager.async_all(
    #                 ScrappingModel.objects.filter(title__icontains=keyword, active=True)
    #             ))

    #         if hotdeals:  # 핫딜이 있는 경우에만
    #             discord_user = await self.fetch_user(user_data['discord_uid'])  # Discord API를 통해 디스코드 유저를 가져옴
    #             if discord_user:  # 유저가 있는 경우에만
    #                 # 메시지 생성: 각 핫딜의 제목과 URL을 포함
    #                 message = "등록된 키워드 검색 결과:\n" + "\n".join(
    #                     [f"{hotdeal.title}: {hotdeal.url}" for hotdeal in hotdeals]
    #                 )
    #                 # 유저에게 메시지를 보냄
    #                 await discord_user.send(message)
    #             else:
    #                 # 유저를 찾을 수 없는 경우 경고 로그를 남김
    #                 logger.warning(f"Could not fetch Discord user for user ID {user.id}")
    #         else:
    #             # 핫딜이 없는 경우 로그를 남김
    #             logger.info(f"No hot deals found for user {user.username}")

            

    # 유저 1이 3개의 키워드가 있으면 액티브가 3칸이 있어서 3번 반복되는 것 같음.
    # async def send_hotdeal_alerts(self):
    #     # 비동기 쿼리를 실행할 수 있도록 비동기 매니저를 사용
    #     async_manager = AsyncManager()

    #     # 활성화된 사용자 객체 가져오기
    #     active_discord_messages = await async_manager.async_all(DiscordMessage.objects.filter(active=True).select_related('user'))

    #     for discord_message in active_discord_messages:
    #         user = await self.fetch_user(discord_message.discord_uid)
    #         keywords = await async_manager.async_all(Keyword.objects.filter(user=discord_message.user))
    #         
            
    #         for keyword in keywords:
    #             hotdeals = []
    #             hotdeals.extend(await async_manager.async_all(ScrappingModel.objects.filter(title__icontains=keyword, active=True)))
    #             logger.info(f"Keyword: {keyword}, Hotdeals: {hotdeals}")
                # for hotdeal in hotdeals:
                    # logger.info(f"Keyword: {keyword}, Hotdeals: {hotdeal}")
                    # await user.send(f"검색 결과: {hotdeal}")
            # for hotdeal in hotdeals:
            #     logger.info(f"Keyword: {keyword}, Hotdeals: {hotdeal}")
                # try:
                #     await user.send(f"검색 결과: {hotdeal}")
                # #     await user.send(f"{keyword} 검색 결과: {hotdeal.url}")
                # #     logger.info(f"Sent hotdeal to {user.name}: {hotdeal.title}")
                # except Exception as e:
                #     logger.error(f"Failed to send hotdeal to {user.name}: {e}")


# Discord 봇 인스턴스 생성
intents = discord.Intents.default()
intents.messages = True
bot = HotdealBot(intents=intents)


async def run_discord_bot():
    await bot.start('MTIxOTE0ODA1MDM1NDgwMjc0OQ.Gl2Gn0.Sc2NGH63or1kELi3pbMCHh7KTHLY_x0Q-IX3Po')

async def main():
    await run_discord_bot()

