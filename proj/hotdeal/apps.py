from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)



class HotdealConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotdeal'
    # # initialized = False  # 초기화 여부를 확인하는 플래그

    # def ready(self):
    #     # if not self.initialized:  # 초기화되지 않았을 때만 실행
    #         # if settings.SCHEDULER_DEFAULT:
    #             from .tasks import start
    #             start()
    #             logger.info("Scheduler started")
    #         # self.initialized = True  # 초기화 완료 후 플래그 설정
