# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # home page after login
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('student/', views.student_booking, name='student'),  # booking page
]
