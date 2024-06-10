from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
    Декоратор для представлений, который проверяет, является ли вошедший в систему пользователь студентом,
    при необходимости перенаправляет на страницу входа.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def lecturer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
    Декоратор для представлений, проверяющий, что вошедший в систему пользователь является учителем,
    при необходимости перенаправляет на страницу входа в систему.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_lecturer or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=Http404):
    """
    Декоратор для представлений, проверяющий, что вошедший в систему пользователь является учителем,
    при необходимости перенаправляет на страницу входа в систему.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
