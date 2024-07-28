from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: #안전한 메소드면, 허용
            return True
        return obj.user == request.user