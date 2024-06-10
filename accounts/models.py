from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

from django.db.models import Q
from PIL import Image

from course.models import Group
from .validators import ASCIIUsernameValidator



class UserManager(UserManager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) | 
                         Q(first_name__icontains=query)| 
                         Q(last_name__icontains=query)| 
                         Q(email__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class User(AbstractUser):
    father_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    is_student = models.BooleanField(default=False, verbose_name='Студент')
    is_lecturer = models.BooleanField(default=False, verbose_name='Преподаватель')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', 
                                default='default.png', null=True, verbose_name="Фото")
    email = models.EmailField(blank=True, null=True, verbose_name="Почта")

    username_validator = ASCIIUsernameValidator()

    objects = UserManager()

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name and self.father_name:
            full_name = self.last_name + " " + self.first_name + " " + self.father_name
        elif self.first_name and self.last_name:
            full_name = self.last_name + " " + self.first_name
        return full_name

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            return "Администратор"
        elif self.is_student:
            return "Студент"
        elif self.is_lecturer:
            return "Преподаватель"

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(level__icontains=query) | 
                         Q(department__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)

    objects = StudentManager()

    def __str__(self):
        return self.student.get_full_name

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)

class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.user)
