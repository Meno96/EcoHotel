from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/logout/', views.logoutUser, name='logout'),
    path('accounts/register/', views.registerPage, name='register'),
    path('consumi/', views.consumiPage, name='consumi'),
    path('user/', views.userPage, name='user'),
    path('home/', views.homePage, name='home'),
]