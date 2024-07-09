from django.test import TestCase
from django.contrib.auth.models import User
from keyword_manager.models import Keyword, DiscordMessage
from keyword_manager.serializers import KeywordSerializer, DiscordMessageSerializer

class KeywordSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')
        self.serializer = KeywordSerializer(instance=self.keyword)

    def test_keyword_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'text']))
        self.assertEqual(data['text'], 'testkeyword')
        '''비교할 데이터의 순서가 중요하지 않은 경우, 
            두 집합의 요소가 동일한지를 간단하게 확인할 수 있기 때문에 set 사용. 
            시리얼라이저의 필드 비교 시 순서는 중요하지 않으므로, 
            set을 사용하여 필드 이름들이 동일한지를 확인'''
    
    def test_keyword_deserialization(self):
        data = {
            'text': 'newkeyword'
        }
        serializer = KeywordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        keyword = serializer.save(user=self.user)
        self.assertEqual(keyword.text, 'newkeyword')
        self.assertEqual(keyword.user, self.user)

class DiscordMessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.keyword = Keyword.objects.create(user=self.user, text='testkeyword')
        self.discord_message = DiscordMessage.objects.create(user=self.user, keyword=self.keyword, active=False)
        self.serializer = DiscordMessageSerializer(instance=self.discord_message)

    def test_discord_message_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['active']))
        self.assertFalse(data['active'])
    
    def test_discord_message_deserialization(self):
        data = {
            'active': True
        }
        serializer = DiscordMessageSerializer(instance=self.discord_message, data=data)
        self.assertTrue(serializer.is_valid())
        discord_message = serializer.save()
        self.assertTrue(discord_message.active)
