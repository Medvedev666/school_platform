from django.urls import path
from .views import *


urlpatterns = [
    # urls групп
    path('', group_view, name='groups'),
    path('<int:pk>/detail/', group_detail, name='group_detail'),
    path('add/', group_add, name='add_group'),
    path('<int:pk>/edit/', group_edit, name='edit_group'),
    path('<int:pk>/delete/', group_delete, name='group_delete'),

    # urls предметов
    path('course/<slug>/detail/', course_single, name='course_detail'),
    path('<int:pk>/course/add/', course_add, name='course_add'),
    path('course/<slug>/edit/', course_edit, name='edit_course'),
    path('course/delete/<slug>/', course_delete, name='delete_course'),

    # urls распределения предметов
    path('course/assign/', CourseAllocationFormView.as_view(), name='course_allocation'),
    path('course/allocated/', course_allocation_view, name='course_allocation_view'),
    path('allocated_course/<int:pk>/edit/', edit_allocated_course, name='edit_allocated_course'),
    path('course/<int:pk>/deallocate/', deallocate_course, name='course_deallocate'),

    # urls загрузки файлов
    path('course/<slug>/documentations/upload/', handle_file_upload, name='upload_file_view'),
    path('course/<slug>/documentations/<int:file_id>/edit/', handle_file_edit, name='upload_file_edit'),
    path('course/<slug>/documentations/<int:file_id>/delete/', handle_file_delete, name='upload_file_delete'),

    path('my_courses/', user_course_list, name="user_course_list"),

    # назначение курса студенту
    path('course/show_assignments/<slug>', submitted_assignments, name="assignments"),
    path('course/add_assignments/<slug>/all/<int:exercise_pk>/', create_add_stud_task, name="add_assignments_all"),
    path('course/add_assignment_one/<slug>/<int:student_id>/<int:exercise_pk>/', create_add_stud_task_one_choice, name="create_add_stud_task_one_choice"),
    path('course/show_students_task', show_students_task, name="show_students_task"),
    path('course/all_students_for_task/<slug>/<int:task_pk>', all_students_for_task, name="all_students_for_task"),
    
    # просмотр результата
    path('show_stud_result/', show_stud_result, name="show_stud_result"),
    path('course/update_mark/<slug>/<int:task_id>/<int:new_mark>', update_mark, name="update_mark"),
]
