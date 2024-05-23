import logging
from apscheduler.schedulers.background import BackgroundScheduler 
from datetime import timedelta
from django.utils import timezone
from .models import ScrappingModel

logger = logging.getLogger(__name__)

  # 백그라운드로 실행해야 함.

def deactivate_olddata():
    threshold_date = timezone.now() - timedelta(hours=48)
    logger.info(f"Deactivating data older than: {threshold_date}")
    old_data_count = ScrappingModel.objects.filter(register_time__lte=threshold_date).count() # 비활성화
    logger.info(f"Found {old_data_count} records to deactivate.")

    if old_data_count > 0:
        ScrappingModel.objects.filter(register_time__lte=threshold_date).update(active=False) # 비활성화
        logger.info("Old data has been deactivated.")  # 작업이 실행되었을 때 로그 메시지 추가
    else:
        logger.info("No old data to deactivate.")


import subprocess

def run_scrapy_crawler():
    # Scrapy 프로젝트 디렉토리로 이동
    scrapy_project_path = 'scrapper_hotdeal'  # Scrapy 프로젝트의 실제 경로로 수정
    scrapy_command = 'scrapy crawl hotdeal'  # 실행할 Scrapy 명령어

    # subprocess를 사용하여 Scrapy 명령어 실행
    try:
        logger.info("Crawling started.")  # 작업이 실행되기 전에 로그 메시지 추가
        subprocess.run(scrapy_command, shell=True, cwd=scrapy_project_path)
        logger.info("Crawling completed.")  # 작업이 완료된 후에 로그 메시지 추가
        deactivate_olddata()  # 크롤링이 끝난 후 데이터 비활성화 작업 실행
    except Exception as e:
        # 실행 중 오류가 발생한 경우 처리
        print(f"Error running Scrapy crawler: {e}")


# 스케줄링 작업 실행
def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(run_scrapy_crawler, 'interval', minutes=1)
    # scheduler.add_job(deactivate_olddata, 'interval', minutes=1)
    scheduler.add_job(run_scrapy_crawler, 'interval', hours=1)
    # scheduler.add_job(deactivate_olddata, 'interval', hours=1)
    try:
      logger.info("Starting scheduler...")
      scheduler.start() # 없으면 동작하지 않습니다.
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")

