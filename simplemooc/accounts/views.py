from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model # para a implementar o código para logar o usuário logo após a conslusão do cadastro
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from simplemooc.courses.models import Enrollment
from .forms import RegisterForm, EditAccountForm, PasswordResetForm # Mesma coisa que: from simplemooc.accounts.forms import RegisterForm
from .models import PasswordReset

User = get_user_model()

@login_required #Decoretor: O método dashboard só será chamado em caso login_required retone true, se não o usuário será encaminhado para a tela de login (atráves do setting LOGIN_URL) e após o login voltará para o form do dashboard (contrariando o setting LOGIN_REDIRECT_URL). Caso queria escolher outra URL para encaminhamento pode-se usar o parâmetro nomeado redirect_field_name do login_required (@login_required(redirect_field_name='my_redirect_field'))
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {}
    #Removido para o usuo de customTemplatesTags. Se a pasta templatetags existir no projetoo Django reconhece os arquivos existentes como Modulos que podem sem utilizados. courses_tags
    #context['enrollments'] = Enrollment.objects.filter(user=request.user)
    return render(request, template_name, context)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1'] # Na senha não se deve usar a variável "user.password" pois é a senha criptrografada (pronta para a persistência na base de dados). No campo "username" também funcionaria assim username=form.cleaned_data['username']
            )
            login(request, user)
            return redirect('core:home')
            #return redirect(settings.LOGIN_URL) #Como usuário logado após o cadastro não é mais necessário redireciona-lo a tela de login após a conclusão
    else:
        #form = UserCreationForm() #método sobreescrito por RegisterForm em forms
        form = RegisterForm() 
    context = {
        'form' : form
    }
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    #Essa abordagem evita o código feito acima (que valida se o método de envio é "POST" para true e caso não envia um form vazio)
        #Analisando o código fonte do Django é visto que o atributo "data" (primeiro parâmetro do método __init__ da class BaseForm arquivo forms.py do código fonto do django) por padrão é "none" e quando o método is_valid() (pode ser consultado no código fonte do django no mesmo local do anterior) é chamado ele verifica se os dados do data estão preenchidos (atraves do is_bound. Ex: self.is_bound) antes de excutar 
            #a validação dos erros (bool.self.erros). No python um durante um "and" se a primeira claúsula for "false" ele não excuta a demais pois (pois não sentido já que para ser "true" todas devem ser "true").
                #Por isso incluindo o "or Nome" evita a validação do campo sem preenchimento (assim que o form é exbido pela primeira vez. Lembrando que sem preenchimento (None) é diferente do form enviado sem dados (sem dados ele será validado))
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)

#Nesse caso será possível usar o form que o Django já possui pronto, nome: SetPasswordForm 
def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)
    	
@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user) #O parâmetro instance é a instância que está sendo alterada (um model). A instância que está sen do alterada é o usuário atual (usuário logado), pode ser acessado através de request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            return redirect('accounts:dashboard')
            #form = EditAccountForm(instance=request.user) #criar um form novammente, vazio #Não mais necessário após o uso redirecionamento(acima)
            #context['sucess'] não mais necessário apos a implantação do uso do sistema de mensagens (aplicado no base.html e na respectiva view)
            #context['sucess'] = True #A cariável sucess passada como verdadeiro no contexto servirá para no template utilziar em um "if" para lançar alguma mensagem ao usuário
    else:
        form = EditAccountForm(instance=request.user) #Se não for POST será retornado apenas um formulário vazio
    context['form'] = form 
    return render(request, template_name, context)

@login_required
#Todo: Implementar validação se a nova senha é igual a atual
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) #Foram passados parämetros nomeados pois se trata de form customizado e náo se sabe ao certo qual a possição dos parâmetros (a menos que a documentação seja consultada)
        if form.is_valid():
            form.save()
            context['sucess'] = True
    else:
        form = PasswordChangeForm(user=request.user)   
    context['form'] = form
    return render(request, template_name, context)      