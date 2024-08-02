from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Health check
    path("", lambda _: HttpResponse("This is 어루만짐!\n")),
    
    # admin 
    path('admin/', admin.site.urls),
    
    path('users/', include('users.urls')),
    path('quest/',include('quest.urls')),
    path('diary/', include('diary.urls')),
    path('selfTest/', include('selfTest.urls')),
    
]
