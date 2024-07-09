from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from keyword_manager.models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

class FilteredAScrappingListViewTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.keyword = 'test'
        self.url = reverse('keyword_manager:filtered_scrapping_list', kwargs={'keyword': self.keyword})
        
        # Create some scrapping models
        ScrappingModel.objects.create(title='test title', active=True)
        ScrappingModel.objects.create(title='another title', active=True)
        
    def test_filtered_scrapping_list(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one object should match
        self.assertEqual(response.data[0]['title'], 'test title')

class KeywordCreateViewTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('keyword_manager:add_keyword')
        self.data = {'text': 'testkeyword'}
        
    def test_create_keyword(self):
        self.authenticate()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Keyword.objects.count(), 1)
        self.assertEqual(Keyword.objects.get().text, 'testkeyword')

class KeywordDeleteViewTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')
        self.url = reverse('keyword_manager:keyword_delete', kwargs={'pk': self.keyword.pk})
        
    def test_delete_keyword(self):
        self.authenticate()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Keyword.objects.count(), 0)

class KeywordListViewTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        Keyword.objects.create(user=self.user, text='keyword1')
        Keyword.objects.create(user=self.user, text='keyword2')
        self.url = reverse('keyword_manager:keyword_list')
        
    def test_list_keywords(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'keyword1')
        self.assertEqual(response.data[1]['text'], 'keyword2')

class DiscordMessageActiveUpdateViewTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')
        self.discord_message = DiscordMessage.objects.create(user=self.user, keyword=self.keyword, active=False)
        self.url = reverse('keyword_manager:active_update', kwargs={'pk': self.discord_message.pk})
        
    def test_update_discord_message_active_status(self):
        self.authenticate()
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.discord_message.refresh_from_db()
        self.assertTrue(self.discord_message.active)
