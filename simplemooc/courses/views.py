#from typing_extensions import Required
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import templatize

from .models import Course, Enrollment, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required
#Quando se utiliza o "." na importação (ex> from .forms) está sendo indicado que é relatóvio a pasta atual (o pacote atual)
#get_object_or_404 : Para tratar quando for selecionado um id de curso que não existe

def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses':courses
    }
    return render(request, template_name, context)

#quando foi usado o id para buscar os cursos
#def details(request, pk ):
#    #course = Course.objects.get(pk=pk)
#    course = get_object_or_404(Course, pk=pk) 
#    context = {
#        'course': course
#    }
#    template_name = 'courses/details.html'
#    return render(request, template_name, context)

def details(request, slug ):
    #course = Course.objects.get(pk=pk)
    course = get_object_or_404(Course, slug=slug)
    #if de valiração se o método de envio é "POST". Se verdadeira passa a requisição via POST se não passa em branco
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            #Para acessar os campos do form é necessário usar o método (que disponibiliza um dicionário) cleaned_data (acessar direatamente não funcionara (ex: Form.name))
            #print(form.cleaned_data)
            #print(form.cleaned_data['name'])
            #print(form.clenead_data['message'])
            form.send_mail(course)
            form = ContactCourse() #Para limpar o formulário após o uso
    else:
        form = ContactCourse() 
    #context = {
    #    'course': course,
    #    'form':  form
    #}
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug) #recuperando o curso atual atráves do campo slug
    #retorna uma tupla (multiplos retornos): A inscrição (se não existrir será criada) e um boleano indicando se foi criado ou não 
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    #Se a inscrição não for encontrada para o curso em questão o método get_or_create vai cria-la e a variável created receberá True. Se True o método active será invocado 
    if created: #trecho necessário pois o valor padrão do campo status foi definido como 0 (zero), se fosse 1 esse trecho não seria necessário
        enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('accounts:dashboard') #método de redirecionamento de URL já utilizado em outros pontos 

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course 
        )
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment':enrollment,
        'course':course,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def announcements(request, slug):
    """
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff: #Caso não seja "staff" verifica a inscrição no curso
        enrollment = get_object_or_404(
            Enrollement, user=request.user, course=course #Parâmetros: Model, usuário e curso
        )
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')
    """
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course':course,
        'announcements':course.announcements.all(), #Linha não necessária pois course já está sendo passado no contexto porém foi incluída para o entendimento ficar mais claro
    }
    return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)            
    #utilizando o request.POST or None evita-se o código que foi feito na views account no método register (Que acaba chamando o método RegisterForm 2 vezes, uma para validar e outro para utilizar caso valido)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        """ 
            "save()" além de salvar o objeto (lembrando que é o "modelForm" que possui o método save(), o "model" não possui), ele cria o objeto, "joga" os valores preenchidos no fórmulário no objeto e retorna o objeto 
                , porém passando o parâmetro "commit=False" ele faz todos os passos mas sem a persistência na base de dados. Util nesse caso pois precisamos passar 
        """
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm() #Invocando um form vazio para limpar o atual (após ser salvo)
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'courses/show_announcement.html'
    context = {
        'course':course,
        'announcement':announcement,
        'form':form,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    if request.user.is_staff:
        lessons = course.lessons.all()
    else:
        lessons = course.release_lessons()
    context = {
        'course':course,
        'lessons':lessons
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    #Somente utilizando a pk já funcionaria porém course foi inclúído como medida de segurança para caso o usuário altere a url e substitua o valor da pk
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template = 'courses/lesson.html'
    context = {
        'course':course,
        'lesson':lesson
    }
    return render(request, template, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    '''Como o material não tem relacionamento com o a curso e sim com a aula (que possui relacionamento com o curso)
       para acessar uma propriedade do objeto relacionado (no caso acessar a pk de lesson que está relacionada com material) é necessário utilizar o duplo underscore "__", lesson__course
    '''
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)        
    if not material.is_embedded():
        return redirect(material.file.url)
    template = 'courses/material.html'
    context = {
        'course':course,
        'lesson':lesson,
        'material':material,
    }
    return render(request, template, context)