from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from venv import logger
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile
from .permissions import CustomReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView 

#회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

#로그인(jwt토큰 발급)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.post(request)  

#로그아웃(jwt토큰)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # refresh token을 블랙리스트에 등록
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # 로그아웃 
# class LogoutView(APIView):  # APIView를 올바르게 사용
#     permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

#     def post(self, request):
#         try:
#             # 토큰이 이미 삭제되었는지 확인
#             if not hasattr(request.user, 'auth_token'):
#                 return Response({"detail": "Already logged out."}, status=status.HTTP_200_OK)
            
#             request.user.auth_token.delete()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# class LogoutView(APIView):  # APIView를 올바르게 사용
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
    
#     def post(self, request):
#         logger.info(f"Logout attempt for user: {request.user}")
#         logger.info(f"Request headers: {request.headers}")
#         logger.info(f"Auth header: {request.META.get('HTTP_AUTHORIZATION')}")

#         if request.auth:
#             try:
#                 request.auth.delete()
#                 logger.info("Token deleted successfully")
#                 return Response({"detail": "로그아웃 성공"}, status=status.HTTP_204_NO_CONTENT)
#             except Exception as e:
#                 logger.error(f"Error during logout: {str(e)}")
#                 return Response({"detail": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             logger.warning("No valid token found")
#             return Response({"detail": "유효한 토큰이 없습니다"}, status=status.HTTP_401_UNAUTHORIZED)

#프로필(mypage)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]

