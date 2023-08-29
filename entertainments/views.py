from authors.forms import LikerPostForm
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from utils.entertainments.factory import make_post

from .models import Entertaiment, Likers

# Create your views here.


def home(request):
    posts = Entertaiment.objects.filter(is_published=True).order_by('-id')
    return render(request, 'entertainments/pages/home.html', context={
        'posts': posts,
    })


def post(request, id):
    # post = Entertaiment.objects.filter(pk=id, is_published=True).order_by('-id').first()

    post = get_object_or_404(Entertaiment, pk=id, is_published=True)

    #Listando Likers
    likers = Likers.objects.filter(post__id=id).order_by('-id')

    this_user_is_liker = False
    #Checando se o usuário atual já é curtidor
    if request.user is not None:
        is_user = Likers.objects.filter(liker__id=request.user.id).order_by('-id').first()
        #Se não for fazio, ele já é curtidos
        if is_user is not None:
            this_user_is_liker = True


    #likers = get_list_or_404(Likers.objects.filter(post=id).order_by('-id'))

    return render(request, 'entertainments/pages/post-view.html', context={
        'post': post,
        'likers': likers,
        'this_user_is_liker':this_user_is_liker,
        'is_detail_page': True,
    })

def category(request, category_id):
    # posts = Entertaiment.objects.filter(category__id=category_id).order_by('-id')

    posts = get_list_or_404(Entertaiment.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'entertainments/pages/category.html', context={
        'posts': posts,
        'title': f'{posts[0].category.name}'
    })
