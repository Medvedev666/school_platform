from django.urls import path

from .views import (
    home_view, post_add, edit_post, delete_post,
    about_view, contact_view
) 


urlpatterns = [
    path('', home_view, name='home'),
    path('add_item/', post_add, name='add_item'),
    path('item/<int:pk>/edit/', edit_post, name='edit_post'),
    path('item/<int:pk>/delete/', delete_post, name='delete_post'),

    path('about/', about_view, name='about'),
    path('contacts/', contact_view, name='contacts'),
]
