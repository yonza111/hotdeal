
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import django
django.setup()
from hotdeal.tasks import start
from discordbot import main
from django.conf import settings
import logging
import subprocess
import asyncio


logger = logging.getLogger(__name__)


def run_discordbot():
    # Scrapy 프로젝트 디렉토리로 이동
    discordbot_path = settings.BASE_DIR  # Scrapy 프로젝트의 실제 경로로 수정
    discordbot_command = 'python discordbot.py'  # 실행할 Scrapy 명령어

    # subprocess를 사용하여 Scrapy 명령어 실행
    try:
        logger.info("discordbot started.")  # 작업이 실행되기 전에 로그 메시지 추가
        subprocess.run(discordbot_command, shell=True, cwd=discordbot_path)
    except Exception as e:
        # 실행 중 오류가 발생한 경우 처리
        print(f"Error running discordbot: {e}")


if __name__ == "__main__":
    start()
    asyncio.run(main())