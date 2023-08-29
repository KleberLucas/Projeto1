from django.urls import path

from entertainments.views import category, home, post

urlpatterns = [
    path('', home, name="entertainments-home"),
    path('posts/<int:id>/', post, name="entertainments-post"),
    path('posts/category/<int:category_id>/', category, name="entertainments-category")
]
