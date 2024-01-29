from .views import LoginView,LogOut, CreateAccount
from django.urls import path

app_name = 'login'

urlpatterns = [
    path('',  LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('create/', CreateAccount.as_view(), name='create'),

]
