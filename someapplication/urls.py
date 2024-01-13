from  django.urls import  path
from .views import CurrentView, IndexView, IndexView2


urlpatterns = [
    path('index1', IndexView2.as_view()),
    path('',IndexView.as_view() ),
    path('datetime/', CurrentView.as_view()),

    ]