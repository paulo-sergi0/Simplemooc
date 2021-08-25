from django.urls import path, re_path
from simplemooc.accounts import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [ 
    re_path(r'^$', views.dashboard, name = 'dashboard'),
    re_path(r'^entrar/$', LoginView.as_view(template_name='accounts/login.html'), name = 'login'),
    re_path(r'^sair/$', LogoutView.as_view(next_page='core:home'), name = 'logout'),
    re_path(r'^cadastre-se/$', views.register, name = 'register'),
    re_path(r'^nova-senha/$', views.password_reset, name = 'password_reset'),
    re_path(r'^confirmar-nova-senha/(?P<key>\w+)', views.password_reset_confirm, name = 'password_reset_confirm'), #Semelhante ao que foi feito no urls.py de courses com o campo slug, no caso será o parâmetro key seguido de um ou mais caracteres
    re_path(r'^editar/$', views.edit, name = 'edit'),
    re_path(r'^editar-senha/$', views.edit_password, name = 'edit_password'),
]
