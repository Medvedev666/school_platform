from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

import datetime

from course.models import Group
# from .models import User, Student, LEVEL
from .models import *


class StaffAddForm(UserCreationForm):
    this_year = datetime.date.today().year

    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Логин", )

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Имя", )

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Фамилия", )
    
    father_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Отчество", )

    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))),
        label="Дата рождения"
    )

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Почта", )

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Пароль", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Подтвердите пароль", )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.father_name = self.cleaned_data.get('father_name')
        user.date_birth = self.cleaned_data.get('date_birth')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    this_year = datetime.date.today().year

    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Логин", )

    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Имя", )

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Фамилия", )
    
    father_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Отчество", )

    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))),
        label="Дата рождения"
    
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), empty_label=None, 
        label="Группа"
    )

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Почта", )

    password1 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Пароль", )

    password2 = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control', }),
        label="Подтвердите пароль", )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.father_name = self.cleaned_data.get('father_name')
        user.date_birth = self.cleaned_data.get('date_birth')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(
            student=user,
            department=self.cleaned_data.get('group')
        )
        student.save()
        return user


class ProfileUpdateForm(UserChangeForm):
    this_year = datetime.date.today().year

    email = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Почта", )


    first_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Имя", )

    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Фамилия", )
    
    father_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        label="Отчество", )

    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))),
        label="Дата рождения"
    )

    class Meta:
        model = User
        fields = ['email', 'date_birth', 'picture', 'first_name', 'last_name', 'father_name']
    
class StudentUpdateForm(UserChangeForm):

    department = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select form-control'}),
        label="Группа",
    )
    
    class Meta:
        model = Student
        fields = ['department']

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "С указанным адресом электронной почты не зарегистрирован ни один пользователь. "
            self.add_error('email', msg)
            return email
