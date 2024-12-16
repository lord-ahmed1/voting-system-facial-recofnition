from django.urls import path
from . import views
urlpatterns=[path("",views.home),path("<str:current_vote>",views.current_vote_handler)]
