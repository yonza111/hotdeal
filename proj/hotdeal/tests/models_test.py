from django.test import TestCase
from unittest import mock
from datetime import datetime, timezone
from ..models import ScrappingModel
from scrapper_hotdeal.scrapper_hotdeal.pipelines import PreprocessingPipeline, SaveToDatabasePipeline
import asyncio

class ScrappingTest(TestCase):
    def setUp(self):
        self.item = {
            'title': '맛도리만두',
            'category': '먹거리',
            'register_time': '10:00',  # 문자열 형태로 시간 받음
            'info': ['마켓', '10,000', '3000원'],
            'url': 'http://url.jrl.jrl'
        }

        # 파이프라인 인스턴스 초기화
        self.preprocessing_pipeline = PreprocessingPipeline()
        self.save_to_db_pipeline = SaveToDatabasePipeline()
        

# (default=timezone.now)

    def test_preprocessing_and_saving_item(self):
        # datetime.now()를 고정된 datetime 객체로 모킹
        fixed_now = datetime(2024, 6, 5, 12, 0)
        with mock.patch('django.utils.timezone.now', return_value=fixed_now):
            # 전처리
            processed_item = self.preprocessing_pipeline.process_item(self.item, None)

            # 비동기 코루틴 실행
            asyncio.run(self.save_to_db_pipeline.process_item(processed_item, None))


        # 테스트 결과
        saved_item = ScrappingModel.objects.get(url='http://url.jrl.jrl')
        print('1111111', saved_item)
        self.assertIsNotNone(saved_item)
        self.assertEquals(saved_item.title, '맛도리만두')
        self.assertEquals(saved_item.category, '먹거리')
        self.assertEquals(saved_item.shop, '마켓')
        self.assertEquals(saved_item.price, '10,000')
        self.assertEquals(saved_item.delivery_fee, '3000원')

        expected_register_time = datetime(2024, 6, 5, 1, 0, tzinfo=timezone.utc)  # UTC 기준 예상 시간
        self.assertEqual(saved_item.register_time, expected_register_time)
        
