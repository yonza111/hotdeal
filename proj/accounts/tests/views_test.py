# accounts/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialToken
from unittest.mock import patch

class DiscordCallbackViewTest(APITestCase):
    
    def setUp(self):
        self.url = reverse('discord_login_callback')  # 테스트할 URL
        self.data = {
            'code': 'mock_code'  # 모의 코드 데이터
        }
        self.user_info = {
            'id': '1234567890',  # 모의 사용자 ID
            'username': 'testuser',  # 모의 사용자 이름
        }
    
    @patch('requests.post')
    @patch('requests.get')
    def test_discord_callback(self, mock_get, mock_post):
        # Mock the response for the token exchange
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access_token': 'mock_access_token'  # 모의 액세스 토큰 설정
        }

        # Mock the response for the user info request
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.user_info # 모의 사용자 정보 설정

        # Send POST request to the Discord callback endpoint
        response = self.client.post(self.url, self.data, format='json')

        # 응답 상태 코드 200(성공)인지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 데이터베이스 유저 생성 확인
        user = User.objects.get(username=self.user_info['username'])
        self.assertIsNotNone(user)

        # 소셜 계정 생성 확인
        social_account = SocialAccount.objects.get(user=user)
        self.assertEqual(social_account.uid, self.user_info['id'])

        # 소셜 토큰 생성 확인
        social_token = SocialToken.objects.get(account=social_account)
        self.assertEqual(social_token.token, 'mock_access_token')

        # 응답 데이터에 JWT 토큰과 사용자 정보가 포함되어 있는지 확인
        response_data = response.json()
        self.assertIn('token', response_data)
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['username'], self.user_info['username'])
