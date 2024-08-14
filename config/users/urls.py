from django.urls import path
from .views import LogoutView, RegisterView, LoginView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃 추가
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
