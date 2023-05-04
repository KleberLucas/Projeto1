from django.urls import path

from entertainments.views import home, post

urlpatterns = [
    path('', home),
    path('posts/<int:id>/', post),
]
