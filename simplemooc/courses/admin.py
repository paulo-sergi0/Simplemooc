from django.contrib import admin
from .models import Course, Enrollment, Announcement, Coment, Lesson, Material

#A classe Admin serve para personalização do Admin
class CourseAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'start_date', 'create_at'] #campos que irão ser exibidos na tela de selecionar o curso
    search_fields = ['name', 'slug'] #A definicação dessa opção cria um campo de texto para a busca e faz um "ou", busca o texto digitado em "name" e "slug"
    prepopulated_fields = {'slug':('name',)} #Opção para preencher automaticamente campos de acordo com outros já preenchidos. Nesse exemplo após o "name" poderiam haver outros campos para composição do texto, ex: ('name', 'descricao')


class MaterialInlineAdmin(admin.TabularInline):#Poderia ser utilizado também a admin.StackedInline, muda a dispozição dos campos exbidos (no painel de admin)

    model = Material


class LessonAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['create_at']

    inlines = [MaterialInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment,Announcement,Coment, Material]) #pode ser feito dessa forma, passando uma lista dde models
admin.site.register(Lesson, LessonAdmin)