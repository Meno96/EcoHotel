from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.accountsPage, name='accounts'),
    path('accounts/login/', views.loginPage, name='login'),
    path('accounts/register/', views.registerPage, name='register'),
    path('consumi/', views.consumiPage, name='home'),
]