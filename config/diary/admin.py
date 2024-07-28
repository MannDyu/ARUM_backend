from django.contrib import admin
from .models import Diary

class DiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content1', 'content2', 'content3')
    search_fields = ('user__username', 'content1', 'content2', 'content3')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)  # created_at 필드를 읽기 전용으로 설정

admin.site.register(Diary, DiaryAdmin)

