기술 스택
프론트엔드: React, JavaScript, CSS
백엔드: Django, Django REST Framework, Gunicorn
데이터베이스: MySQL
서버: Nginx
웹 스크래핑: Scrapy
배포: Docker, Docker Compose

### 주요 기능
- **실시간 핫딜 스크래핑**: 주기적으로 스크래핑 작업을 수행하여 핫딜 정보를 수집하고 표시.
- **키워드 관리**: 사용자가 관심 키워드를 생성, 수정 및 삭제할 수 있으며, 키워드별로 핫딜 정보를 필터링하여 제공.
- **Discord 알림 연동**: Discord 봇을 통해 핫딜 알림을 제공하며, 사용자가 Discord 알림 설정을 관리 가능.
- **사용자 인증**: Discord OAuth2를 사용하여 사용자 인증 및 로그인 관리.
- **프론트엔드**: React를 사용하여 직관적이고 반응형 사용자 인터페이스 제공.
- **백엔드**: Django REST Framework와 MySQL을 기반으로 API 제공 및 데이터 관리.