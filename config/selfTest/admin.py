from django.contrib import admin
from .models import Hospital,Self_test,Self_test_result,Search_center

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Self_test)
admin.site.register(Self_test_result)
admin.site.register(Search_center)