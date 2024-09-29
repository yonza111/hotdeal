### 사용된 기술 스택
- **프론트엔드**: React, JavaScript, CSS
- **백엔드**: Django, Django REST Framework, Gunicorn
- **데이터베이스**: MySQL
- **서버**: Nginx
- **웹 스크래핑**: Scrapy
- **배포**: Docker, Docker Compose

### 주요 기능
- **실시간 핫딜 스크래핑**: Scrapy 이용한 주기적인 핫딜 정보 스크래핑.
- **키워드 관리**: 사용자가 관심 키워드를 생성 및 삭제할 수 있으며, 키워드별로 핫딜 정보를 필터링하여 검색 가능.
- **Discord 알림 연동**: Discord 봇을 통해 키워드로 등록된 핫딜 알림 제공, 알림 설정 On/Off 기능 제공.
- **사용자 인증**: Discord OAuth2를 통한 사용자 인증 및 로그인 관리.
- **Unittest**: Django unittest를 통한 테스트 기능.