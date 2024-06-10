from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import NewsAndEvents
from .forms import NewsAndEventsForm
from accounts.decorators import admin_required

def home_view(request):
    items = NewsAndEvents.objects.all()
    

    context = {
        'title': 'МАОУ "СОШ № 47 г. Улан-Удэ',
        'items': items
    }
    return render(request, 'news/index.html', context)

@login_required
@admin_required
def post_add(request):
    if request.method == 'POST':
        print(f'{request.FILES=}')
        form = NewsAndEventsForm(request.POST, request.FILES)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, ('Новость ' + title + ' была добавлена.'))
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста исправьте ошибки.')
    else:
        form = NewsAndEventsForm()
    return render(request, 'news/post_add.html', {
        'title': 'Добавление новости',
        'form': form,
    })

@login_required
@admin_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == 'POST':
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get('title')
        if form.is_valid():
            form.save()

            messages.success(request, ('Новость ' + title + ' была обновлена.'))
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста исправьте ошибки.')
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(request, 'news/post_add.html', {
        'title': 'Редактирование поста',
        'form': form,
    })


@login_required
@admin_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, ('Новость ' + title + ' была удалена.'))
    return redirect('home')


def contact_view(request):
    context = {
        'title': 'Контакты || МАОУ "СОШ № 47 г. Улан-Удэ',
    }
    return render(request, 'news/contacts.html', context)

def about_view(request):
    context = {
        'title': 'О школе || МАОУ "СОШ № 47 г. Улан-Удэ',
    }
    return render(request, 'news/about.html', context)