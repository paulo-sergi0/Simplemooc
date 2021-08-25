from django.urls import path, re_path
from simplemooc.courses import views

app_name = 'courses'

urlpatterns = [ 
    re_path(r'^$' , views.index, name = 'index'),
    #re_path(r'^(?P<pk>\d+)/$' , views.details, name = 'details'), #quando foi usado o id para buscar os cursos
    re_path(r'^(?P<slug>[\w_-]+)/$' , views.details, name = 'details'),
    re_path(r'^(?P<slug>[\w_-]+)/inscricao/$' , views.enrollment, name = 'enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$' , views.undo_enrollment, name = 'undo_enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/$' , views.announcements, name = 'announcements'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)$' , views.show_announcement, name = 'show_announcement'), #passando como parâmetro a chave primaria e a validando com expressão regular (\d+ = um ou mais números)
    re_path(r'^(?P<slug>[\w_-]+)/aulas/$' , views.lessons, name = 'lessons'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)$$' , views.lesson, name = 'lesson'),
    re_path(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)$$' , views.material, name = 'material'),
]

#(?P<pk>\d+) : A expressão regular "\d+" o resto serve pra agrupar/nomear expressões regulares. Nomeação é utill pra o caso de existerem mais de um parâmetro (possiveis problemas com a ordem de envio dos parâmetros)