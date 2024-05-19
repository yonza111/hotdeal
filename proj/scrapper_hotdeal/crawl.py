import os
from scrapy import cmdline
import logging

logger = logging.getLogger(__name__)

def run_scrapy_crawler():
    # 현재 스크립트의 디렉토리 경로
    crawl_directory = os.path.dirname(os.path.abspath(__file__))
    proj_directory = os.path.abspath(os.path.join(crawl_directory, '..', '..'))

    # crawl.py가 위치한 디렉토리에서 스크래피 실행
    os.chdir(crawl_directory)
    
    try:
        logger.info("Crawling started.")  # 작업이 실행되기 전에 로그 메시지 추가
        cmdline.execute("scrapy crawl hotdeal".split())
        logger.info("Crawling completed.")  # 작업이 완료된 후에 로그 메시지 추가
    finally:
        os.chdir(proj_directory)



# from scrapy import cmdline
# import logging
# logger = logging.getLogger(__name__)
# def run_scrapy_crawler():
#     logger.info("Crawling started.")  # 작업이 실행되기 전에 로그 메시지 추가
#     cmdline.execute("scrapy crawl hotdeal".split())
#     logger.info("Crawling completed.")  # 작업이 완료된 후에 로그 메시지 추가