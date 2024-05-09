# scrapy 주기적 실행과 db에 일정 시간 지난 데이터들 비활성화 하는 2개 함수 만들기.

from apscheduler.schedulers.background import BackgroundScheduler 

scheduler = BackgroundScheduler()  # 백그라운드로 실행해야 함.


def scrapy_crawling():  # scrapy 실행 
    pass


# 스케줄링 작업 등록
scheduler.add_job(scrapy_crawling, 'interval', hours=3)


# 스케줄링 작업 실행
scheduler.start()