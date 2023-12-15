from django.urls import URLPattern, path
from apps.core.views import TodolistView, UsersView


urlpatterns: list[URLPattern] = [
    path("users/<int:user_id>/todos/items/", TodolistView.as_view(), name="todolist"),
    path("users/", UsersView.as_view(), name="users"),
]
