# ARUM_backend


### 1. 프로젝트 클론
git clone <repository-url>
cd <project-directory>

### 2. 가상 환경 설정
python -m venv venv

###가상 환경 활성화 (운영 체제에 따라 선택)
source venv/bin/activate       # Linux/MacOS
.\venv\Scripts\activate        # Windows

### 3. 패키지 설치
pip install -r requirements.txt

### 4. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

### 5. 슈퍼유저 생성 (선택 사항)
python manage.py createsuperuser

### 6. 서버 실행
python manage.py runserver
