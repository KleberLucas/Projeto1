from django.http import HttpResponse
from django.shortcuts import render
from utils.entertainments.factory import make_post

# Create your views here.


def home(request):
    return render(request, 'entertainments/pages/home.html', context={
        'posts': [make_post() for _ in range(10)],
    })


def post(request, id):
    return render(request, 'entertainments/pages/post-view.html', context={
        'post': make_post,
    })
