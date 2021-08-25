from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User #import removido pois essa referência é ao usuário padrão do Django, como ele foi customizado sempre que necessário utilizar a classe usuário o a funcão "get_user_model" deverá ser utilziada
from django.contrib.auth import get_user_model #assim estamos apontando ao Django para ulitzar o "novo padrão" (defino em settings AUTH_USER_MODEL = 'accounts.User')
from .models import PasswordReset
from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template


User = get_user_model()

##removido por falta de compatibilidade após a customização do model de usuários
""" class RegisterForm(UserCreationForm): # Como foi criado um modelo customizado de usuário é necessário reescrever o UserCreationForm pois ele depende do user padrão do Django (informação disponívelna documentação)

    email = forms.EmailField(label='E-mail') #incluindo o field no form

    def clean_email(self): #método chamado "automaticamente", quando o Django vai fazer a validaçao dos campos ele procura métodos com o nome clean_NomeDoCampo, se retornar alguma execção ele e passada ao form que solictou a validação
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe usuário com este E-mail')
        return email 
        
    #Sobreescrevendo o método save da class UserCreationForm (https://github.com/django/django/blob/stable/3.1.x/django/contrib/auth/forms.py)
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False) #usando o "super" o método save de UserCreationForm (pois foi passado como parâmetro na criação da class) é chamado. Commit=false para não salvar os dados até o email ser preenchido 
        user.email = self.cleaned_data['email'] #cleanned_data é um dicionário retornado após a chamada do save com dos os dados do form preenchidos/válidados/normalidados como um objeto python
        if commit: #Na situação atual o commit poderia ser omitido (tanto do parâmetro de save quanto na linha atual), porém foi mantido pois da margem a possibilidade(além de manter uma certa compatibilidade com o método base) de herdar o RegisterForm e manipular os dados antes de salvar
            user.save()
        return user    
"""

#Uncialmente será um form comum (não será um ModelFomr, ou seja não estará associado diretamente a um model) pois só é necessário um campo de e-mail 
class PasswordResetForm(forms.Form):
    
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():#Semelhante a cláusula exists do banco de dados, retornará um boolean caso o e-mail exista no banco de dados
            return email
        raise forms.ValidationError(
            'Nehum usuário encotrado com este e-mail'
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email']) #o .get é um filer que retorna apenas obejetos, se não retornar nada é gerada um execção
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Simple MOOC'
        context = {
            'reset':reset,
        }
        send_mail_template(subject, template_name, context,[user.email])


class RegisterForm(forms.ModelForm): # Como foi criado um modelo customizado de usuário é necessário reescrever o UserCreationForm pois ele depende do user padrão do Django (informação disponívelna documentação)

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não está correta') #code='password_mismatch', #O ValidationError aceita o envio desse código(como parâmetro), testar posteriormente
        return password2
                
    """
    Método baseado no save padrão do Djando (consultado o código fonte do Django)
    O método set_password em django/contrib/auth/forms.py criptrografa a senha antes de envia-la ao banco de dados
    A codificação pode ser verificada no código fonte do django disponível no github (https://github.com/django/django/blob/stable/3.1.x/django/contrib/auth/forms.py)
    """
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False) #Chamada do save do RegisterForm (atráves do "super") com commit=false para não salvar (isso feito para utilizar o método "set_password" que a encriptação da senha)
        user.set_password(self.cleaned_data['password1']) #Com o usur retornado a senha e setada e salva (commit=true)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):
    """
    Método removido por não fazer mais sentido validar a unicidade do e-mail após a customização do model de usuários (pois lá foi definido como único no banco de dados)
    ToDO: será mostrado mais a frente no curso como personalizar o método clean_email afim de não repedir o código

    def clean_email(self): 
        email = self.cleaned_data['email']
        É necessário excluir o usuário atual (usuário logado) da busca do e-mail em utilização pois se o usuário não mudar o e-mail durante a edição sempre haverá um usuário com esse e-mail em uso.
        A variável instance, todo o ModelForm possui. Se o usuário não estiver editando algum dado esse váriavel será "none", mas esse form só será utilizado apenas para editção de um usuário que já existe a veriável (instance) sempre estará dispónivel.
        O método exclude é como um filtro inverso (como um "not in"). Assim será verificado em todos os usuários cadastrados(execto o usuário em questão que está sendo alterado) se o novo e-mail a ser inserido já existe
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk) # A variável queryset foi criada apenas para facilitar o entendimento do procedimento, não é obrigatório, poderia ter sido incluida antes .exists() no if abaixo   
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este E-mail')
        return email
        ToDo: Pesquisar sobre exclude(pk=self.instance.pk) pois não está alterando em nada o comportamento com relação ao e-mail (fazer mais testes pra confirmar)
    """
    class Meta: # Para o Djando saber para qual model que esse formulário irá é a classe Meta é necessária junto do atributo Model
        model = User
        #removido após a customização do model de usuários
        #fields = ['username', 'email', 'first_name', 'last_name'] #Fiels são os campos que estarão disponíveis no formumário para edição do usuário. Incialmente serão utilizados os campos que o Django fornece (['username', 'emial', 'first_name', 'last_name'])
        fields = ['username', 'email', 'name']
       
    