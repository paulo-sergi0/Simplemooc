"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin 
from django.urls import path, include, re_path
#from simplemooc.core import views
#from simplemooc.core import urls
#re_path - Para usar expressões regulares
from django.conf import settings
from django.conf.urls.static import static

app_name = 'simplemooc'

#Obs: a / no final é opcional. O django busca url que o usuário mandou caso não encontre ele redireciona com barra (/)
urlpatterns = [ 
    re_path(r'^', include('simplemooc.core.urls')),
    re_path(r'^conta/', include('simplemooc.accounts.urls')),
    re_path(r'^cursos/', include('simplemooc.courses.urls')),
    #re_path(r'^$' , views.home, name = 'home'),
    #re_path(r'^contato/$', views.contact, name = 'contact'),
    path('admin/', admin.site.urls),
]

#Se estiver no modeo debug carregar as imagens
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)