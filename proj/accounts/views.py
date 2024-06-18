import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def discord_callback(request):
    if request.method == 'POST':
        code = request.data.get('code')
        if code:
            # 디스코드 API로부터 받은 인가 코드를 사용하여 액세스 토큰을 요청하고, 해당 토큰을 가져오는 역할
            access_token = get_access_token(code)
            if access_token:
                user_info = get_user_info(access_token)
                print(user_info)

                user = get_or_create_user_from_discord(user_info, access_token)
                user_data = UserSerializer(user).data
                
                # JWT 토큰 생성
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                print('user_data :', user_data)
                return Response({
                    'user': user_data,
                    'token': access_token  # JWT 토큰 추가
                })
    
    return Response({'error': 'Invalid request'}, status=400)


def get_access_token(code):
    token_url = 'https://discord.com/api/oauth2/token'
    client_id = '1219148050354802749'
    client_secret = 'lNt2oFQ9YqJfbMEAcLPe89QNuoKXr3aU'
    redirect_uri = 'http://127.0.0.1:3000/auth/'
    
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
        return response.json().get('access_token')
    else:
        response.raise_for_status()


def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
 
    response = requests.get('https://discord.com/api/users/@me', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_or_create_user_from_discord(user_info, access_token):
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
