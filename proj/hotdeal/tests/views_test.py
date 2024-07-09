from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import ScrappingModel
from django.utils import timezone

class ScrappingListViewTest(APITestCase):
    def setUp(self):
        self.item1 = ScrappingModel.objects.create(
                title='테스트1',
                category='전자제품',
                register_time=timezone.now(),
                shop = '슈퍼마켓',
                price = '10000',
                delivery_fee = '3000',
                url='https://test-url.com',
                active = True
            )
        self.item2 = ScrappingModel.objects.create(
                title='테스트2',
                category='먹거리',
                register_time=timezone.now(),
                shop = '슈퍼마켓',
                price = '30000',
                delivery_fee = '3000',
                url='https://test-url.com',
                active = True
            )

    def test_scrapping_list_view(self):
        url = reverse('hotdeal:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # 결과 리스트가 비어 있지 않은지 확인
        self.assertEqual(len(response.data), 2) # active=True인 것만 리턴하는지 확인
        for item in response.data:
            self.assertTrue(item['active'])


    def test_category_list_view(self):
        url = reverse('hotdeal:category_list', kwargs={'category': '전자제품'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # 전자제품, active=True만 리턴하는지 확인
        for item in response.data:
            self.assertEqual(item['category'], '전자제품')
            self.assertTrue(item['active']) 


    def test_scrapping_search_list(self):
        url = reverse('hotdeal:search')
        response = self.client.get(url, {'q': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('search: ',response.data)
        self.assertEqual(len(response.data), 1) # title에 2 들어가고 active=True만 리턴하는지 확인
        for item in response.data:
            self.assertIn('2', item['title'])
            self.assertTrue(item['active'])  

    
    def test_scrapping_detail(self):
        url = reverse('hotdeal:detail', kwargs={'pk': self.item2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('detail: ', response.data)
        self.assertEqual(response.data['title'], '테스트2') # 목표 데이터를 리턴하는지?
