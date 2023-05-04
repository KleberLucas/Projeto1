from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'entertainments/pages/home.html', context={
        'name': 'Kleber Lucas',
    })


def post(request, id):
    return render(request, 'entertainments/pages/post-view.html')
