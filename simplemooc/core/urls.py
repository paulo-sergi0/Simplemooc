from django.urls import path, re_path
from simplemooc.core import views

app_name = 'core'

urlpatterns = [ 
    re_path(r'^$' , views.home, name = 'home'),
    re_path(r'^contato/$', views.contact, name = 'contact'),
    #path('' , views.home, name='home'),
    #path('contato/', views.contact, name='contact'),
]