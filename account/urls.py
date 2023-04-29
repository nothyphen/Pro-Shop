from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_web, name='login'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_web, name="logout"),
]