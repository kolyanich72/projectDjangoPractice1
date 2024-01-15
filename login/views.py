from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User




class LoginView(View):

    def get(self, request):
        return render(request,"login/index.html")

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store:shop')  #при ок аутентиф-и редирект на стр shop
        return  redirect('login:login')# redirect('login:login')             #JsonResponse(request.POST, json_dumps_params={"indent":4})


class LogOut(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('store:shop')


class CreateAccount(View):

   def get(self, request):
       return render(request, "login/create_account.html")


   def post(self, request):
       form = CustomUserCreationForm(data=request.POST)
       if form.is_valid():
           username = form.cleaned_data.get('username')
           email = form.cleaned_data.get('email')
           password = form.cleaned_data.get('password1')
           user = User.objects.create_user(username=username, email=email, password=password)
           user.save()
           login(request, user)
           return redirect('store:shop')
       return render(request, 'login:create',context={'error':form.errors})



