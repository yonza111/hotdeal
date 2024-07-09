from django.test import TestCase
from django.contrib.auth.models import User
from keyword_manager.models import Keyword, DiscordMessage
from allauth.socialaccount.models import SocialAccount

class KeywordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')

    def test_keyword_creation(self):
        self.assertEqual(self.keyword.text, 'testkeyword')
        self.assertEqual(self.keyword.user.username, 'testuser')

class DiscordMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')
        self.discord_message = DiscordMessage.objects.create(user=self.user, keyword=self.keyword, active=False)

    def test_discord_message_creation(self):
        self.assertEqual(self.discord_message.user.username, 'testuser')
        self.assertEqual(self.discord_message.keyword.text, 'testkeyword')
        self.assertFalse(self.discord_message.active)

    def test_create_discord_uid(self):
        # SocialAccount 객체를 생성합니다.
        social_account = SocialAccount.objects.create(user=self.user, provider='discord', uid='123456')

        # DiscordMessage의 create_discord_uid 메서드를 호출하여 UID를 가져옵니다.
        discord_uid = DiscordMessage.create_discord_uid(self.user)
        self.assertEqual(discord_uid, '123456')
