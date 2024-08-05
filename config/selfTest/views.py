from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from django.db.models import Q
from datetime import date
from .models import Self_test, Self_test_result,Hospital
from .models import Search_center

## 테스트 점수 받아서 디비에 저장하고 결과 뿌려주는 기능
## case1) 자가 테스트 처음 -> 디비에 새로운 행 추가(insert)
## case2) N번째 자가 테스트 -> 해당 유저의 데이터 디비에서 찾아서 새로운 값으로 업데이트 
class scoreSaveAndGetResult(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        test_score = request.data.get('test_score')

        if test_score is None:
            return Response({"error": "Test score is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            test_score = int(test_score)
        except ValueError:
            return Response({"error": "Invalid test score value"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Self_test 테이블에서 해당 유저의 레코드가 있는지 확인
            self_test, created = Self_test.objects.get_or_create(user_id=user, defaults={'test_score': test_score, 'test_date': date.today()})

            if not created:
                # 해당 유저의 레코드가 이미 있는 경우, test_score와 test_date 업데이트
                self_test.test_score = test_score
                self_test.test_date = date.today()
                self_test.save()

            # 해당 점수에 맞는 결과를 Self_test_result 테이블에서 조회
            test_result = Self_test_result.objects.get(min_score__lte=test_score, max_score__gte=test_score)

            response_data = {
                "test_score": self_test.test_score,
                "result_subheading": test_result.result_subheading,
                "result_content": test_result.result_content,
                "result_image": test_result.result_image.url if test_result.result_image else None, ##result_image는 이미지 파일의 경로를 저장, 이를 URL로 변환하여 응답에 포함
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Self_test_result.DoesNotExist:
            return Response({"error": "No result found for the given score"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## 해당 유저의 마지막 자가 테스트 날짜 가져옴
class getSelfTestDate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = self.request.user.id

        try:
            # Self_test 테이블에서 해당 유저의 레코드 조회
            self_test = Self_test.objects.get(user_id=user_id)
            response_data = {
                "test_date": self_test.test_date
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Self_test.DoesNotExist:
            return Response({"error": "No test record found for the user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## 센터 찾기 
## case1) 서울 강남구의 센터 정보 가져옴 (필터 걸기전에 기본으로 보여줄 정보)
class getCenterInfo(APIView):
    def get(self,request):
        search_terms = ["서울", "강남구"]
        
        # Filter hospitals where hp_address contains both "서울" and "강남"
        hospitals = Hospital.objects.filter(
            Q(hp_address__icontains=search_terms[0]) & Q(hp_address__icontains=search_terms[1])
        )

        hospital_data = [{"hp_name": hospital.hp_name, "hp_address": hospital.hp_address, "hp_phone": hospital.hp_phone} for hospital in hospitals]

        return Response(hospital_data, status=status.HTTP_200_OK)
    ## 센터 검색시 하나의 구만 검색할 수 있는 경우
    # def post(self, request):
    #     term1 = request.data.get('term1')
    #     term2 = request.data.get('term2')

    #     if not term1 or not term2:
    #         return Response({"error": "Both term1 and term2 are required"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Filter hospitals where hp_address contains both term1 and term2
    #     hospitals = Hospital.objects.filter(
    #         Q(hp_address__icontains=term1) & Q(hp_address__icontains=term2)
    #     )

    #     hospital_data = [
    #         {"hp_name": hospital.hp_name, "hp_address": hospital.hp_address, "hp_phone": hospital.hp_phone}
    #         for hospital in hospitals
    #     ]

    #     return Response(hospital_data, status=status.HTTP_200_OK)
    
    ## 센터 검색시 최대 3개 구까지 검색할 수 있는 경우
    def post(self, request):
        city = request.data.get('city')
        district1 = request.data.get('district1')
        district2 = request.data.get('district2')
        district3 = request.data.get('district3')
        if not city or not district1:
            return Response({"error": "City and District1 are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the base query
        query = Q(hp_address__icontains=city) & Q(hp_address__icontains=district1)

        # Optionally add district2 and district3 to the query
        if district2:
            query |= Q(hp_address__icontains=city) & Q(hp_address__icontains=district2)
        if district3:
            query |= Q(hp_address__icontains=city) & Q(hp_address__icontains=district3)

        hospitals = Hospital.objects.filter(query).distinct()

        hospital_data = [
            {"hp_name": hospital.hp_name, "hp_address": hospital.hp_address, "hp_phone": hospital.hp_phone}
            for hospital in hospitals
        ]

        return Response(hospital_data, status=status.HTTP_200_OK)
    
## 검색 필터 지역구 불러오기
class getDistrict(APIView):
    def post(self,request):
        city = request.data.get('city')

        if not city:
            return Response({"error": "City parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 주어진 city 값으로 Search_center 테이블에서 데이터 필터링
        centers = Search_center.objects.filter(city=city)
        
        if not centers.exists():
            return Response({"error": "No records found for the given city"}, status=status.HTTP_404_NOT_FOUND)
        
        # QuerySet을 직렬화하여 결과 반환
        # serializer = SearchCenterSerializer(centers, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
        districts = [center.district for center in centers]
        return Response({"districts": districts}, status=status.HTTP_200_OK)
