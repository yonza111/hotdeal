import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User
from .serializers import UserSerializer
import os
from dotenv import load_dotenv

load_dotenv()

class DiscordCallbackView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        code = request.data.get('code')
        if code:
            access_token = self.get_access_token(code)
            if access_token:
                user_info = self.get_user_info(access_token)
                print(user_info)

                user = self.get_or_create_user_from_discord(user_info, access_token)
                user_data = UserSerializer(user).data
                
                # JWT 토큰 생성
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                
                print('user_data :', user_data)
                return Response({
                    'user': user_data,
                    'token': token  # JWT 토큰 추가
                })
        
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token(self, code):
        token_url = 'https://discord.com/api/oauth2/token'
        client_id = os.getenv('DISCORD_CLIENT_ID')
        client_secret = os.getenv('DISCORD_CLIENT_SECRET')  # 수정: 잘못된 환경 변수명 수정
        # redirect_uri = 'http://127.0.0.1:3000/auth/'
        redirect_uri = 'http://localhost/auth/'
        
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'scope': 'identify email'
        }

        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            print('rrrrr성공')
            return response.json().get('access_token')
        else:
            print(f"Error: {response.status_code} - {response.text}")  # 디버깅용
            response.raise_for_status()

    def get_user_info(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
    
        response = requests.get('https://discord.com/api/users/@me', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_or_create_user_from_discord(self, user_info, access_token):
        discord_uid = user_info.get('id')
        username = user_info.get('username')
        
        social_account_qs = SocialAccount.objects.filter(uid=discord_uid)
        
        if social_account_qs.exists():
            return social_account_qs.first().user
        
        user = User.objects.create_user(username=username)
        
        social_account = SocialAccount.objects.create(
            user=user,
            uid=discord_uid,
            provider='discord'
        )
        
        SocialToken.objects.create(
            account=social_account,
            token=access_token
        )
        
        return user
    