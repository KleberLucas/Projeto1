from django.urls import path

from entertainments.views import home, post

urlpatterns = [
    path('', home, name="entertainments-home"),
    path('posts/<int:id>/', post, name="entertainments-post"),
]
