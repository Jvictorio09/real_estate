# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.lesson6, name="lesson6"),
    path("lesson-6/<slug:slug>/", views.lesson_detail, name="lesson_detail"),
    path("api/chat", views.chat_proxy, name="chat_proxy"),

    path("webhook/<uuid:token>", views.espo_webhook, name="espo_webhook"),
]