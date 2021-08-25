import re #Módulo de regex
from django.db import models
from django.core import validators #Lista de validação de campos de formulário dispoveis (uso visto no código fonte do Django na camada de usuário padrão(contrib.auth - AbstractUser))
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
#AbstractBaseUser: Possui a lógica pronta de alterar senha, cripitrografar senha e comportamentos base de usuários. Dois campos uteis (pois faz sentido para a aplicação atual) que esse import traz são: Senha e last_login
#PermissionsMixin: Segurança do Django, permissões de grupos(qie o adimin também usa)
#UserManager: Traz implementações de funcões do Django na parte de usuários(ex: como criação de super usuário, dentro outros). Ele é um manage, como foi feita a implementação de um custom manage (no model da app de cursos (course), class CourseManage, e foi colocado como Objects) 
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile(r'^[\w.@+-]+\Z'), #validators é uma lista que validaçãoes que pode ser passada ao field. #Regex diferente a exibida na aula, foi obtida no código fonte do django
            'O nome de usuário só pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_', 'invalid')] #RegexValidator possui 3 parâmetros: o regex a ser testado, a mensagem a ser exibida no caso do retorno "false"  e um código "invalid" servirá para o fórmulário no momento da validação 
    )
    email = models.EmailField('E-mail', unique=True) #O e-mail agora é único (diferentemente do usuário padrão do Django)
    name = models.CharField('Nome', max_length=100, blank=True)
    #Abaixo são campos para que o admin(do django) funcione perfeitamente. Não são obrigatórios mas facilitão a implementação além de serem realmente uteis. Esses campos estão na app padrão de usuários do Django (class AbstractUser), porém nela possuem campos que não são uteis para a aplicação atual (como last_name, first_name além do campo de e-mail não ser obrigaptório)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True) #Boleano para indicar se o usuário está ativo ou não (se pode logar ou não), como comentado esté é um campo que o usuário padrão do Django possui e ele é utilizado em alguns pontos (por isso fica mais fácil utiliza-lo do que customizar os pontos de utilização)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=True) #Serve para o Django admin discernir usuários que podem ou não acessar a área administrativa. Verificar a necesisade pois quem faz esse controle é o campo "is_superuser"
    date_joined = models.DateField('Data de Entrada', auto_now=True) #Data de criação do usuário (importante para a criação de superUser), necessário cria-la para a compatibilidade com com a app de usuários do Django
        #auto_now_add=True : Quando o esse valor for salvo pela primeira vez a data atual será persistida
        #auto_now=True : Toda vez que o usuário é modificado a data é salva
    
    objects = UserManager()

    #Variáveis necessárias para a compatibilidade de alguns comandos do Django (da app de usuário)
    USERNAME_FIELD = 'username' #Indicação do campo unico, o campo que é a referência na hora do login. Por padrão é o username mas pode ser alterado se necessáiro (ex: email)
    REQUIRED_FIELDS = ['email'] #É utilizado no comando de criaçao de super usuário. (quando o banco for apagado/hora da implantação e produção esse comando será utilizado)

    #Método para retornar a representação em string do nome do usário
    def __str__(self):
        return self.name or self.username #Se houver nome será retornado se não o username

    #get_short_name e get_full_name métodos não obrigatórios mas uteis para o funcionamento pleno da app de usuários do Django
    def get_short_name(self):
        return self.username #Descrição curta do nome
    
    def get_full_name(self):
        return str(self) #Será a representação string do próprio objeto, que quando chamado executará o méotodo sobreescrito (logo acima) "__str__" que é o mome do usuário
    
    class Meta: #Mesma classe criada na app de cursos (courses). Será importante para o admin
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

"""
Ao fim da criação dessa class é necessário a alteração da variável AUTH_USER_MODEL em settings.py

Novo model com relacionamento de N:1 com User
Quando um model possui uma Foreign Key para outro model (no caso model User), o Django automaticamente cria um atribuito no model "pai" (no caso model User) com o nome seguindo o padrão: Nome do model (no caso PasswordReset) todo minusculo seguido de "_set" (ficando passwordreset_set).
    Caso não queria seguir esse nome padrão a variável related_name deve ser prenchida              
        O objetivo do atributo é retornar o outro lado da relação que seria um usuário possui 1 ou mais resets de senha (a relação do lado da que possui a foring key é um resete de senha possui um usuário)
"""
class PasswordReset(models.Model):
    """
    user = models.ForeignKey(User) #Normalmente somente o parâmetro User (Model) seria necessário porém como estamos utilziand a app padrão de usuário do Django 
        é necessário utilizar o settings AUTH_USER_MODEL
    """    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        on_delete = models.CASCADE, #não exibido na aula mas obrigatório nas novas versões do Django
        related_name='resets'
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at'] #Parâmetro que pode ser passado para definição da ordenção padrão, no caso será pelo campo "created_at" descrescente (definido pelo "-")