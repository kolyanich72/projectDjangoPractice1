from django.shortcuts import render
from django.views import View
import datetime
from  django.http import  HttpResponse
#from .templates.someapplication import

class CurrentView(View):
    def get(self, request):
        str_ = datetime.datetime.now().strftime('%H:%M:%S %A, %d. %B %Y')
        html_response = f"{str_}"
        return HttpResponse(html_response)


class IndexView2(View):
    def get(self, request):
        return render(request, 'index1.html')

class IndexView(View):
    def get(self, request):
        return render(request, 'someapplication/index.html')

# Create your views here.
