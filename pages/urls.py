from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video_list/', views.video_list, name='video_list'),
]