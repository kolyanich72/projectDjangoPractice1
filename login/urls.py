from .views import LoginView,LogOut
from django.urls import path

app_name = 'login'

urlpatterns = [
    path('',  LoginView.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),

]
