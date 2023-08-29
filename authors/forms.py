import re
from collections import defaultdict

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from entertainments.models import Entertaiment, Likers


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
            code='invalid'
        )

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        required= True,
        widget=forms.PasswordInput(attrs= {
            'placeholder': 'Digite sua senha'
        }),
        validators=[strong_password]
    )
    

    confirmPassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs= {
            'placeholder': 'Repita sua senha'
        }),
        error_messages= {
            'required': "Não pode ser vazia"
        }
        
    )

    class Meta:
        model= User
        fields= ['first_name', 'last_name', 'username', 'email', 'password']
        #Usamos o dicionário "labels" que já vem do Django para configurar o nome dos labels
        # labels ={
        #     'username': "Digite seu usuário:",
        # }
        #Usamos o dicionário "help_texts" que já vem do Django para configurar as mensagens de ajuda
        help_texts ={
            'email': "Este campo é obrigatório!",
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Digite o nome de usuário"
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': "Digite a sua senha"
            })
        }

    #Quando vamos validar apenas um campo, utilizamos clean_nomeDoCampo
    def clean_email(self):
        #Salva o email passado no formulário
        email = self.cleaned_data.get('email', '')
        #Faz uma busca para ver se já existe o email passado
        exists = User.objects.filter(email=email)

        # Se existir...sobe o erro
        if exists:
            raise ValidationError('O E-mail já está em uso', code='invalid')
        return email

    # Método para validação de mais de um campo (No caso password e confirmPassword)
    def clean(self):
        #cleaned_data é o dado já tratado pelo Django (Campo Limpo)
        cleaned_data = self.cleaned_data
        #Pegando os campos e salvar em variável. Na função get colocamos o nome do campo
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        #validando e comparando. Se são diferentes
        if password != confirmPassword:
            #Chama um erro de validação por serem diferentes
            raise ValidationError({
                #Dessa forma o erro vai aparecer abaixo dos dois campos:
                'password':'As senhas não são iguais',
                'confirmPassword':'As senhas não são iguais'
            })

class LoginForm(forms.Form):
    #Criando os campos colocando que são obrigatórios (required)
    #E configurando seus placeholder
    username = forms.CharField(
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    #E configurando seus placeholder
    widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Digite o nome de usuário"
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': "Digite a sua senha"
            })
        }


class AuthorPostForm(forms.ModelForm):
    #__init__ é o método construtor da classe
    #Pelo campo nós adicionarmos um atributo "class" que é a classe para configurarmos no CSS
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._my_errors = defaultdict(list)

            self.fields["review"].widget.attrs.update({"class": "span-2"})
            self.fields["cover"].widget.attrs.update({"class": "span-2"})
    
    class Meta:
        
        #O model é o model que importamos lá em cima
        model = Entertaiment
        fields = 'title', 'description', 'note', 'company', 'review', 'cover', 'category'
       
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        #Pegamos os dados limpos passados no formulário
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        #Se o título é igual a descrição, mostramos os erros:

        if title == description:
            self._my_errors['title'].append('Não pode ser igual à descrição')
            self._my_errors['description'].append('Não pode ser igual ao título')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Deve ter pelo menos 5 caracteres.')

        return title

    def clean_note(self):
        field_name = 'note'
        field_value = self.cleaned_data.get(field_name)
        #Se é numero negativo

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('O número deve ser positivo')

        return field_value

#Função que tenta converter um número (para saber se não foi escrito texto)
#E se é positivo.
def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0


class LikerPostForm(forms.ModelForm):
    class Meta:
        
        #O model é o model que importamos lá em cima
        model = Likers
        fields = 'post','liker'
