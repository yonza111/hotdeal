# discordbot.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import django
django.setup()
import discord
import logging
import asyncio
from keyword_manager.models import DiscordMessage
from hotdeal.models import ScrappingModel
from django.db.models import Manager
from asgiref.sync import sync_to_async
import os
from dotenv import load_dotenv
from datetime import timedelta
from django.utils import timezone

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # 기본 로깅 설정

def deactivate_olddata():
    threshold_date = timezone.now() - timedelta(hours=48)
    logger.info(f"Deactivating data older than: {threshold_date}")
    old_data_count = ScrappingModel.objects.filter(register_time__lte=threshold_date).count()
    logger.info(f"Found {old_data_count} records to deactivate.")

    if old_data_count > 0:
        ScrappingModel.objects.filter(register_time__lte=threshold_date).update(active=False)
        logger.info("Old data has been deactivated.")
    else:
        logger.info("No old data to deactivate.")

deactivate_olddata()

class AsyncManager(Manager):
    async def async_all(self, queryset):
        return await sync_to_async(list)(queryset)


class HotdealBot(discord.Client):
    async def on_ready(self):
        logger.info(f'We have logged in as {self.user}')
        await self.send_hotdeal_alerts()
        await self.close()
        logging.info("send_hotdeal_alerts executed and bot is closing.")

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
            embeds = []  # 유저별로 보낼 임베드 메시지를 저장할 리스트

            for keyword in keywords:  # 각 유저의 키워드들을 순회
                # 키워드에 해당하는 핫딜들을 가져옴
                hotdeals = await async_manager.async_all(
                    ScrappingModel.objects.filter(title__icontains=keyword, active=True)
                )
                if hotdeals:  # 핫딜이 있는 경우에만
                    embed = discord.Embed(
                        title=f"'{keyword}' 검색 결과",
                        description="",
                        color=discord.Color.blue()
                    )
                    for hotdeal in hotdeals:
                        embed.add_field(
                            name=f"({hotdeal.title}    {hotdeal.price})",
                            value=hotdeal.url,
                            inline=False
                        )
                    embeds.append(embed)  # 임베드 리스트에 추가

            if embeds:  # 임베드가 있는 경우에만
                discord_user = await self.fetch_user(user_data['discord_uid'])  # Discord API를 통해 디스코드 유저를 가져옴
                if discord_user:  # 유저가 있는 경우에만
                    for embed in embeds:
                        await discord_user.send(embed=embed)  # 각 임베드를 유저에게 전송
                else:
                    # 유저를 찾을 수 없는 경우 경고 로그를 남김
                    logger.warning(f"Could not fetch Discord user for user ID {user.id}")
            else:
                # 핫딜이 없는 경우 로그를 남김
                logger.info(f"No hot deals found for user {user.username}")


# Discord 봇 인스턴스 생성
intents = discord.Intents.default()
intents.messages = True
bot = HotdealBot(intents=intents)


async def run_discord_bot():
    await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

async def main():
    await run_discord_bot()

if __name__ == "__main__":
    logger.info("Starting discordbot.py")
    asyncio.run(main())
    logger.info("Finished discordbot.py")




