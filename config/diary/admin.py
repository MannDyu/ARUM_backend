from django.contrib import admin
from .models import Diary

class DiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'feel' ,'emotion', 'tag1', 'tag2', 'tag3')
    search_fields = ('user__username', 'content1', 'content2', 'content3')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

admin.site.register(Diary, DiaryAdmin)

