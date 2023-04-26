from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def contato(request):
    return HttpResponse("<h1>CONTATO</h1>")


def sobre(request):
    return HttpResponse("<h1>SOBRE</h1>")
