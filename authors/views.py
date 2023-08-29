from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from entertainments.models import Entertaiment

from .forms import AuthorPostForm, LikerPostForm, LoginForm, RegisterForm


# Create your views here.
def register_view(request):
    #Dessa forma é criado uma variável com o mesmo nome do valor de session
    #Caso seja vazio vem None (Por isso de none após a vírgula)
    #Get = pegar é o contrário do POST, mas ai ele já está pegando os dados. Pois o redirect é GET
    register_form_data = request.session.get('register_form_data', None)

    #Ai é passado as informações para dentro do Form da página
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()
        
    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    #Verificar se é válido o formulário: Se sim, salva
    if form.is_valid():
        data = form.save(commit=False)
        password = request.POST['password']
        data.password = make_password(data.password)
        data.save()
        #Mensagem de sucesso (precisa de importação lá em cima)
        messages.success(request, 'Seu usuário foi criado, por favor faça o login')
        # Limpa a Session
        del(request.session['register_form_data'])
        return redirect(reverse('authors-login'))


    return redirect('authors-register')


def login_view(request):
    #O 'form' são os campos que criamos no LoginForm
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors-login-create')
    })

def login_create(request):
    
    #Se não vier post (Método de passar dados) volta com erro
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)
    #Variável recebe o redirecionamento ao login
    login_url = reverse('authors-login')

    #Se o formulário de login é valído, então ele vai autenticar e logar
    if form.is_valid():
        #Faz a checagem
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        #Se é verdadeiro, se está autenticado e existe o usuário
        if authenticated_user is not None:
            messages.success(request, 'Sucesso, você logou')
            #Loga o usuário após o sucesso
            login(request, authenticated_user)
            
        else:
        #Se deu errado a autenticação ele faz:
            messages.error(request, 'Usuário ou senha estão incorretos')
            
    else:
    #E se o form não é inválido
    #Então se chegou até aqui é porque deu errado e não deu o return
        messages.error(request, "Credenciais Inválidas")


    return redirect(reverse('authors-dashboard'))

#Ela é uma página restrita, só pode ser acessada se o usuário estiver de fato já logado
#O Login required faz a view existir e funcionar só quando o usuário estiver logado
#Login_url é a página que o site joga se o usuário tentar acessar deslogado
@login_required(login_url='authors-login', redirect_field_name='next')
def logout_view(request):
    #Não aceita se vier método GET
    #Se não for método POST:
    if not request.POST:
        #Se for outro método, redirecionado ao login de volta
        return redirect(reverse('authors-login'))
        
    # mais outra parede de segurança, também checa se o usuário que está deslogando existe no sistema
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors-login'))

    #Usamos a função que importamos de logout
    logout(request)
    #Redirecionado para o Login
    return redirect(reverse('authors-login'))


@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard(request):
    #Busca pelos posts NÃO PUBLICADOS e que o author é o usuário logado
    posts = Entertaiment.objects.filter(is_published=False, author=request.user)
    return render(request, 'authors/pages/dashboard.html', context={
        'posts':posts,
    })


@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_post_edit(request, id):
    #Recebe o ID que foi clicado para editar
    #Só pode editar se NÃO FOI PUBLICADO
    #Se é do usuário logado
    post = Entertaiment.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not post:
        raise Http404()

    form = AuthorPostForm(
        #Já vem com as informações preenchidas OU(or) Vazio
        request.POST or None,
        #E salvamos os arquivos se são diferentes, é sempre  necessário quando trabalhamos com ARQUIVOS
        files=request.FILES or None,
        #Passamos à instância a postagem buscada lá em cima (Variável post)
        instance=post
    )

    if form.is_valid():
        # Agora, o form é válido e eu posso tentar salvar
        #Passamos save commit false para ele não salvar de uma vez, pois ainda iremos fazer inserção de dados.
        post = form.save(commit=False)

        # Completando informações que o usuário não controla
        post.author = request.user
        post.review_is_html = False
        post.is_published = False

        post.save()

        #E assim enviamos uma mensagem de sucesso
        messages.success(request, 'Sua postagem foi salva com sucesso!')
        #O args é como passar um valor na URL, no caso será o próprio ID da postagem (Do <int:id>)
        return redirect(reverse('authors-dashboard-post-edit', args=(id,)))

    return render(
        request,
        'authors/pages/dashboard_entertainment.html',
        context={
            'post':post,
            'form':form,
        }
    )

@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_post_new(request):
    form = AuthorPostForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        post: Entertaiment = form.save(commit=False)

        post.author = request.user
        post.review_is_html = False
        post.is_published = False

        post.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('authors-dashboard-post-edit', args=(post.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_entertainment.html',
        context={
            'form': form,
            'form_action': reverse('authors-dashboard-post-new')
        }
    )

@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_post_delete(request):

     #Se não vier como post bugará:
    if not request.POST:
        raise Http404()

    #Buscando o id agora, o que foi passado via post no input.
    POST = request.POST
    id = POST.get('id')

    #Busca o post correto para deletar, após descobrir o id via post
    post = Entertaiment.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    #Onde deletamos de fato
    post.delete()
    messages.success(request, 'Postagem deletada com sucesso.')
    #Volta para o dashboard
    return redirect(reverse('authors-dashboard'))


@login_required(login_url='authors-login', redirect_field_name='next')
def dashboard_post_like(request):
    form = LikerPostForm()
    #Se não vier como post bugará:
    if not request.POST:
        raise Http404()

    #Buscando o id agora, o que foi passado via post no input.
    POST = request.POST
    post_id = POST.get('post_id')
    liker_id = POST.get('liker_id')

    #Busca o post correto para curtir, após descobrir o id via post
    post = Entertaiment.objects.filter(
        is_published=True,
        pk=post_id,
    ).first()

    #Busca o user correto que é curtidor
    user = User.objects.filter(
        pk=liker_id,
    ).first()

    
    post_liker = form.save(commit=False)

        # Completando informações que o usuário não controla
    post_liker.post = post
    post_liker.liker = user

    post_liker.save()
    messages.success(request, 'Curtiu a postagem')
    #Volta para a postagem normal
    return redirect(reverse('entertainments-post', args=(post.id,)))

   
    
    
    #Volta para o dashboard
    
