from django.urls import path

from entertainments.views import home

urlpatterns = [
    path('', home),
]
