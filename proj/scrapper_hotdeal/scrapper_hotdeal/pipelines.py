# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from hotdeal.models import ScrappingModel
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from django.utils import timezone
import logging



class ScrapperHotdealPipeline:
    def process_item(self, item, spider):
        return item

class PreprocessingPipeline:    # 데이터 전처리
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        self.logger.info(f"Processing item: {item}")
        item['title'] = self.clean_title(item['title'])
        item['register_time'] = self.clean_register_time(item['register_time'])
        self.logger.info(f"After processing: {item}")

        return item

    def clean_title(self, title):
        cleaned_title = title.replace('\t', '').replace('\xa0', '').strip()
        self.logger.debug(f"Cleaned title: {cleaned_title}")

        return cleaned_title

    def clean_register_time(self, register_time):
        cleaned_register_time = register_time.replace('\t', '').strip()
        self.logger.debug(f"Cleaned register_time: {cleaned_register_time}")

        now = timezone.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        current_date = now.strftime('%Y-%m-%d')
        yesterday_date = now - timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime('%Y-%m-%d') 
        if int(cleaned_register_time[:2]) > int(current_hour):
            cleaned_register_time = datetime.strptime((yesterday_date_str + ' ' + cleaned_register_time), '%Y-%m-%d %H:%M')
        elif int(cleaned_register_time[:2]) < int(current_hour):
            cleaned_register_time = datetime.strptime((current_date + ' ' + cleaned_register_time), '%Y-%m-%d %H:%M')
        elif int(cleaned_register_time[:2]) == int(current_hour) and int(cleaned_register_time[-2:]) < int(current_minute):
            cleaned_register_time = datetime.strptime((current_date + ' ' + cleaned_register_time), '%Y-%m-%d %H:%M')
        else:
            cleaned_register_time = datetime.strptime((yesterday_date_str + ' ' + cleaned_register_time), '%Y-%m-%d %H:%M')

        self.logger.debug(f"After datetime parsing: {cleaned_register_time}")

        return cleaned_register_time


class SaveToDatabasePipeline:   # 데이터 저장
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @sync_to_async
    def process_item(self, item, spider):
        self.logger.info(f"Processing item to save: {item}")

        title = item.get('title')
        category = item.get('category')
        register_time = item.get('register_time')
        info = item.get('info')
        url = item.get('url')

        if not ScrappingModel.objects.filter(url=url).exists(): # url을 id로 사용해서 중복 시 저장안되게
            ScrappingModel.objects.create(
                title=title,
                category=category,
                register_time=register_time,
                shop = info[0],
                price = info[1],
                delivery_fee = info[2],
                url=url
            )
            self.logger.info(f"Item saved successfully: {item}")
        else:
            self.logger.info(f"Item already exists, not saving: {item}")

        return item
 