# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from hotdeal.models import ScrappingModel
from datetime import datetime


class ScrapperHotdealPipeline:
    def process_item(self, item, spider):
        return item

class PreprocessingPipeline:
    def process_item(self, item, spider):
        # 각 필드에 대한 전처리 수행
        item['title'] = self.clean_title(item['title'])
        item['register_time'] = self.clean_register_time(item['register_time'])

        return item

    def clean_title(self, title):
        cleaned_title = title.replace('\t', '').replace('\xa0', '').strip()
        return cleaned_title

    # def clean_register_time(self, register_time):
    #     cleaned_register_time = register_time.replace('\t', '').strip()
    #     time_format = "%H:%M"
    #     now = datetime.now()
    #     current_time = now.strftime("%H:%M")

    #     return cleaned_register_time
    

class SaveToDatabasePipeline:
    def process_item(self, item, spider):
        title = item.get('title')
        category = item.get('category')
        register_time = item.get('register_time')
        info = item.get('info')
        url = item.get('url')

        # 데이터 저장
        ScrappingModel.objects.create(
            title=title,
            category=category,
            register_time=register_time,
            shop = info[0],
            price = info[1],
            delivery_fee = info[2],
            url=url
        )

        return item
 

# 날짜 로직
# 중복 처리? 이건 걍 앞에서 url로 처리해보자
## 현재 시간이 15시인데 등록 시간이 17:xx이다? 이러면 어제 날짜 넣는거지. 이거 이전이면(0시~14시) -> 오늘 날짜 넣고.
## 그리고 register_time의 글자가 몇 글자 이상이면 뭐 종료 이런식으로 페이지 넘어가서 스크래핑하게 만들자(\t때문에 len은 7이 됨. 8 이상이면 종료)