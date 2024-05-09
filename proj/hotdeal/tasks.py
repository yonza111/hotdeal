# scrapy 주기적 실행과 db에 일정 시간 지난 데이터들 비활성화 하는 2개 함수 만들기.

from apscheduler.schedulers.background import BackgroundScheduler 
from scrapper_hotdeal.crawler import run_scrapy_crawler
from datetime import timedelta
from django.utils import timezone
from .models import ScrappingModel

scheduler = BackgroundScheduler()  # 백그라운드로 실행해야 함.

def deactivate_olddata():
    threshold_date = timezone.now() - timedelta(hours=48)
    ScrappingModel.objects.filter(created_at__lte=threshold_date).update(active=False) # 비활성화


# 스케줄링 작업 등록
scheduler.add_job(run_scrapy_crawler, 'interval', hours=3)
scheduler.add_job(deactivate_olddata, 'cron', hour=23, minute=50)


# 스케줄링 작업 실행
try:
    scheduler.start()
except KeyboardInterrupt:
    scheduler.shutdown()