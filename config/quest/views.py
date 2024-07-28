import random
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from datetime import date,datetime


## 퀘스트 분야 버튼 누르면 quest테이블에 있는 정보 랜덤으로 하나 불러오는 API (요청 url: http://127.0.0.1:8000/quest/randomQuest/(hb,cl,ex,me,dy중 하나)/)
## 수행 step
## 1. 화면단에서 퀘스트 분야 선택
## 2. 화면애서 선택한 분야에 맞는 미션 하나 랜덤으로 디비에서 가져옴
## 3. 내부적으로 랜덤 미션 history테이블에 저장
## 4. 랜덤 값 리턴
class RandomQuest(APIView) :

    def get(self, request, qs_theme): #url의 파라미터로 전달시 여기서 매개변수로 받음
        if qs_theme not in ['dy', 'cl', 'ex', 'me', 'hb']:
            return Response({"error": "Invalid qs_theme"}, status=status.HTTP_400_BAD_REQUEST)
        
        quests = Quest.objects.filter(qs_theme=qs_theme) #퀘스트 테이블에서 qs_theme가 요청 들어온 테마인 것 모두 quests변수에 저장
        if not quests.exists():
            return Response({"error": "No quests found for the given qs_theme"}, status=status.HTTP_404_NOT_FOUND)
        
        random_quest = random.choice(quests) #해당 테마의 퀘스트 중 랜덤으로 하나 뽑음
        serializer = QuestSerializer(random_quest) # 해당 모델 값 serializer해서 serializer변수에 저장
        
        # Quest_history에 저장 (랜덤으로 오늘의 미션 생성하고 내부적으로 history테이블에 생성된 미션 저장)
        quest_history = Quest_history(
            user_id= 90000, #request.user.id,  # 인증된 사용자라면 request.user.id 사용
            qs_theme=random_quest.qs_theme,
            qs_content=random_quest.qs_content
        )
        quest_history.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK) #serializer된 데이터 리턴

## 미션완료하면 인증글,사진,미션 수행여부 디비에 업데이트
class UpdateQuestHistory(APIView):
    ## 수정이랑 포스트 둘 다 같은 로직 수행 so, 로직 함수로 빼고 post,put분기
    def post(self,request):
        user_id = 90000
        # user_id = request.data.get('user_id')
        # if not user_id:
        #     return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update_quest_history(request, user_id)
    
    def put(self,request):
        user_id = 90000
        # user_id = request.data.get('user_id')
        # if not user_id:
        #     return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        return self.update_quest_history(request, user_id)
    
    def update_quest_history(self, request,user_id):
        print(f"Request data: {request.data}")  # 디버깅을 위해 추가
        
        try:
            quest_history = Quest_history.objects.get(user_id=user_id, qs_date=date.today())
        except Quest_history.DoesNotExist:
            return Response({"error": "Quest history not found for the given user and date"}, status=status.HTTP_404_NOT_FOUND)

        quest_history.qs_perform_yn = True
        quest_history.qs_perform_content = request.data.get('qs_perform_content', quest_history.qs_perform_content) ##클라이언트가 제출한 폼 데이터에서 qs_perform_content 값을 가져옵니다. 만약 클라이언트가 이 값을 제출하지 않았다면, 기본값으로 두 번째 인수인 quest_history.qs_perform_content를 사용
        
        if 'qs_perform_image' in request.FILES:
            quest_history.qs_perform_image = request.FILES['qs_perform_image']
        
        quest_history.save()

        serializer = QuestHistorySerializer(quest_history)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


## 히스토리 테이블의 모든 정보 불러옴
class QuestList(APIView) :
    def get(self, request):
        questList = Quest_history.objects.all()
        serializer  = QuestHistorySerializer(questList,many=True)
        return Response(serializer.data)
    
## 해당 회원이 해당 월에 수행한 미션 리스트 정보(날짜만 필요) 가져오기 수행여부도 같이 필요?????
## 화면에서 날짜 어떻게 줄지몰라 둘 다 구현 프론트랑 상의후 하나 지워야함
class MonthlyQuestList(APIView):
    def get(self, request, year, month):
        user_id = 90000
        # user_id = request.data.get('user_id')
        # if not user_id:
        #     return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            start_date = datetime(year=int(year), month=int(month), day=1)
            end_date = datetime(year=int(year), month=int(month)+1, day=1) if month != 12 else datetime(year=int(year)+1, month=1, day=1)
            
            quest_dates = Quest_history.objects.filter(
                user_id=user_id, 
                qs_date__gte=start_date, 
                qs_date__lt=end_date
            ).values_list('qs_date', flat=True)
            
            return Response(list(quest_dates), status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        user_id = 90000
        # user_id = request.data.get('user_id')
        year = request.data.get('year')
        month = request.data.get('month')

        if not user_id or not year or not month:
            return Response({"error": "user_id, year, and month are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime(year=int(year), month=int(month), day=1)
            end_date = datetime(year=int(year), month=int(month)+1, day=1) if int(month) != 12 else datetime(year=int(year)+1, month=1, day=1)
            
            quest_histories = Quest_history.objects.filter(user_id=user_id, qs_date__gte=start_date, qs_date__lt=end_date).values_list('qs_date', flat=True)
            serializer = QuestHistorySerializer(quest_histories, many=True)
            return Response(list(quest_dates), status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid year or month"}, status=status.HTTP_400_BAD_REQUEST)
        
## 해당 회원이 해당 날짜에 수행한 미션 정보 가져오기
## 화면에서 날짜 어떻게 줄지몰라 둘 다 구현 프론트랑 상의후 하나 지워야함
class SpecificQuestInfo(APIView):
    def get(self, request, year, month,day):
        user_id = 90000
        # user_id = request.data.get('user_id')
        # if not user_id:
        #     return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            qs_date = datetime(year=int(year), month=int(month), day=int(day))
            
            quest_history = Quest_history.objects.filter(user_id=user_id, qs_date=qs_date)
            
            serializer = QuestHistorySerializer(quest_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        user_id = 90000  # 임시 user_id 값
        year = request.data.get('year')
        month = request.data.get('month')
        day = request.data.get('day')

        if not year or not month or not day:
            return Response({"error": "Year, month, and day are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qs_date = datetime(year=int(year), month=int(month), day=int(day))
            
            quest_history = Quest_history.objects.filter(user_id=user_id, qs_date=qs_date)
            
            serializer = QuestHistorySerializer(quest_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)