from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView

from .models import User, Student

PasswordResetView.reset_password_form = None

class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'username', 'email', 'is_active', 'is_student', 'is_lecturer', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_lecturer', 'is_staff']

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'




admin.site.register(User, UserAdmin)
admin.site.register(Student)
