# hotdeal/models.py

from django.db import models
from django.utils import timezone
# 핫딜 스크래핑 해온거 저장하는 모델
class ScrappingModel(models.Model):
    # 제목, 가격, 카테고리, 쇼핑몰, 배송, 등록시간, url
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    shop = models.CharField(max_length=20)
    delivery_fee = models.CharField(max_length=20)
    register_time = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
