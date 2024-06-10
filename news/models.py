from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse


class NewsAndEvents(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", validators=[
                               MinLengthValidator(3, message="Минимум 3 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('posts', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'
        ordering = ['-time_create', 'title']
