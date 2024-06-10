from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from .decorators import admin_required
from course.models import Course
from .forms import StaffAddForm, StudentAddForm, ProfileUpdateForm, StudentUpdateForm
from .models import User, Student




def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)


def register(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Профиль успешно создан.")
        else:
            messages.error(
                request, f"Что-то не так, пожалуйста, заполните все поля правильно."
            )
    else:
        form = StudentAddForm(request.POST)
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    """Show profile of any user that fire out the request"""

    if request.user.is_lecturer:
        courses = Course.objects.filter(
            allocated_course__lecturer__pk=request.user.id
        )
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "courses": courses,
            },
        )
    elif request.user.is_student:
        level = Student.objects.get(student__pk=request.user.id)

        context = {
            "title": request.user.get_full_name,
            "level": level,
        }
        return render(request, "accounts/profile.html", context)
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "staff": staff,
            },
        )


@login_required
def profile_single(request, id):
    """Show profile of any selected user"""

    if request.user.pk == id:
        return redirect("profile")
    
    user = User.objects.get(pk=id)
    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id)
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "Lecturer",
            "courses": courses,
        }
        return render(request, "accounts/profile_single.html", context)
    elif user.is_student:
        student = Student.objects.get(student__pk=id)

        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "student",
            "student": student,
        }
        return render(request, "accounts/profile_single.html", context)
    else:
        context = {
            "title": user.get_full_name,
            "user": user,
            "user_type": "superuser",
        }
        return render(request, "accounts/profile_single.html", context)


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль был успешно обновлен.")
            return redirect("profile")
        else:
            print(f'{form.errors=}')
            messages.error(request, "Пожалуйста исправьте ошибки ниже.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(
        request,
        "setting/profile_info_change.html",
        {
            "title": "Настройка профиля",
            "form": form,
        },
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Ваш пароль был обновлен!")
            return redirect("profile")
        else:
            messages.error(request, "Пожалуйста исправьте ошибки ниже. ")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "setting/password_change.html",
        {
            "form": form,
        },
    )


@login_required
@admin_required
def staff_add_view(request):
    if request.method == "POST":
        form = StaffAddForm(request.POST)
        first_name = request.POST.get("first_name")
        father_name = request.POST.get("father_name")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Профиль для преподавателя "
                + first_name
                + " "
                + father_name
                + " был успешно создан.",
            )
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()

    context = {
        "title": "Добавить преподавателя",
        "form": form,
    }

    return render(request, "accounts/add_staff.html", context)


@login_required
@admin_required
def edit_staff(request, pk):
    instance = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, "Преподаватель " + full_name + " был обновлен.")
            return redirect("lecturer_list")
        else:
            messages.error(request, "Пожалуйста исправьте ошибки ниже.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_lecturer.html",
        {
            "title": "Редактировать преподавателя",
            "form": form,
        },
    )


@method_decorator([login_required, admin_required], name="dispatch")
class LecturerListView(ListView):
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Преподаватели"
        return context


@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, "Преподаватель " + full_name + " был удален.")
    return redirect("lecturer_list")



@login_required
@admin_required
def student_add_view(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Профиль для " + first_name + " " + last_name + " был успешно создан.",
            )
            return redirect("student_list")
        else:
            messages.error(request, "Исправьте ошибки ниже.")
    else:
        form = StudentAddForm()

    return render(
        request,
        "accounts/add_student.html",
        {"title": "Добавить студента", "form": form},
    )


@login_required
@admin_required
def edit_student(request, pk):
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        student_form = StudentUpdateForm(request.POST, instance=instance.student)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()
            student_form.save()
            messages.success(request, ("Профиль студента " + full_name + " был обновлен."))
            return redirect("student_list")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибку ниже.")
    else:
        form = ProfileUpdateForm(instance=instance)
        student_form = StudentUpdateForm(instance=instance.student)
    return render(
        request,
        "accounts/edit_student.html",
        {
            "title": "Редактировать профиль",
            "form": form,
            "student_form": student_form,
        },
    )


@method_decorator([login_required, admin_required], name="dispatch")
class StudentListView(ListView):
    template_name = "accounts/student_list.html"
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        queryset = Student.objects.all()
        query = self.request.GET.get("student_id")
        if query is not None and query != '':
            queryset = queryset.filter(Q(department=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Студенты"
        return context


@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, "Студент был удален.")
    return redirect("student_list")



