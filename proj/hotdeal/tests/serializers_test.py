from django.test import TestCase
from hotdeal.models import ScrappingModel
from hotdeal.serializers import HotdealScrappingModelSerializer
from datetime import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo

class HotdealScrappingModelSerializerTest(TestCase):
    def setUp(self):
        # 테스트용 데이터 생성
        self.data = {
            'title': '제로치킨',
            'category': '전자제품',
            'register_time': timezone.now(),
            'shop': '슈퍼마켓',
            'price': '10000',
            'delivery_fee': '3000',
            'url': 'https://test-url.com',
            'active' : True
        }

        self.scrapping_model_instance = ScrappingModel.objects.create(**self.data)
        self.serializer = HotdealScrappingModelSerializer(instance=self.scrapping_model_instance)
        # print(self.serializer.data)

    def test_serializer_contains_expected_fields(self): 
        # fields 테스트
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'title', 'category', 'register_time', 'shop', 'price', 'delivery_fee', 'url', 'active'])

    def test_serializer_field_content(self):
        # serialization 테스트
        data = self.serializer.data
        self.assertEqual(data['title'], self.data['title'])
        self.assertEqual(data['category'], self.data['category'])
        self.assertEqual(data['shop'], self.data['shop'])
        self.assertEqual(data['price'], self.data['price'])
        self.assertEqual(data['delivery_fee'], self.data['delivery_fee'])
        self.assertEqual(data['url'], self.data['url'])
        self.assertEqual(data['active'], self.data['active'])

        # register_time을 동일한 타임존으로 변환하여 비교
        kst = ZoneInfo('Asia/Seoul')
        expected_register_time = self.data['register_time'].astimezone(kst).isoformat()
        self.assertEqual(data['register_time'], expected_register_time)
        ''' Serializer 테스트에서는 주로 데이터베이스 모델 객체를 직렬화하여 얻은 결과가 
            예상대로 JSON 형식으로 반환되는지를 확인합니다. 
            이 때 UTC로 변환된 시간 필드를 테스트하는 것이 일반적입니다.'''

    def test_valid_data_creates_scrapping_model(self):
        # deserialization 테스트 - 지금 앱에는 필요 없는 듯
        serializer = HotdealScrappingModelSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        scrapping_model = serializer.save()
        self.assertIsNotNone(scrapping_model.id)
        self.assertEqual(scrapping_model.title, self.data['title'])
        self.assertEqual(scrapping_model.category, self.data['category'])
        self.assertEqual(scrapping_model.shop, self.data['shop'])
        self.assertEqual(scrapping_model.price, self.data['price'])
        self.assertEqual(scrapping_model.delivery_fee, self.data['delivery_fee'])
        self.assertEqual(scrapping_model.url, self.data['url'])
        self.assertEqual(scrapping_model.active, self.data['active'])
        self.assertEqual(scrapping_model.register_time, self.data['register_time'])
        ''' Deserializer 테스트에서는 주로 입력 데이터를 정확히 파싱하여 
            데이터베이스에 저장되는지를 확인합니다. 
            이 과정에서는 Serializer에서처럼 UTC 타임존 변환을 테스트하지 않는 경우가 많습니다.'''
        
    def test_invalid_data(self):
        # 유효성 검사
        invalid_data = self.data.copy() # 수정할 수 있는 데이터 사본
        invalid_data['price'] = ''  

        serializer = HotdealScrappingModelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

