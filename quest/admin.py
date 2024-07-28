from django.contrib import admin
from .models import Quest
from .models import Quest_history

# Register your models here.
admin.site.register(Quest)
admin.site.register(Quest_history)