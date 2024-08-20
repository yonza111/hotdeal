# scrapy.py
import os
import django
import logging
# from datetime import timedelta
# from django.utils import timezone

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()

# # Django 설정이 초기화된 후에 모델을 임포트
# from hotdeal.models import ScrappingModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # 기본 로깅 설정

# def deactivate_olddata():
#     threshold_date = timezone.now() - timedelta(hours=48)
#     logger.info(f"Deactivating data older than: {threshold_date}")
#     old_data_count = ScrappingModel.objects.filter(register_time__lte=threshold_date).count()
#     logger.info(f"Found {old_data_count} records to deactivate.")

#     if old_data_count > 0:
#         ScrappingModel.objects.filter(register_time__lte=threshold_date).update(active=False)
#         logger.info("Old data has been deactivated.")
#     else:
#         logger.info("No old data to deactivate.")

import subprocess

def run_scrapy_crawler():
    scrapy_project_path = 'scrapper_hotdeal'
    scrapy_command = 'scrapy crawl hotdeal'

    try:
        logger.info("Crawling started.")
        subprocess.run(scrapy_command, shell=True, cwd=scrapy_project_path)
        logger.info("Crawling completed.")
        # deactivate_olddata()
    except Exception as e:
        print(f"Error running Scrapy crawler: {e}")

if __name__ == "__main__":
    logger.info("Starting scrapy.py")
    run_scrapy_crawler()
    logger.info("Finished scrapy.py")