from django.template import Library
register = Library() #Comando para "registrar" o import acima
from simplemooc.courses.models import Enrollment

#Tipos de templatetags
    #inclusion_tag: Serve para renderizar um template parcial em algum ponto
    #simple_tag: Serve para testar alguma lógica e retornar algo (textom,hmtl.. ou algo do tipo)

@register.inclusion_tag('courses/templatetags/my_courses.html')
#função para retornar os cursos de um usuário
#Usa o my_courses.html - Porém não está em uso
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments': enrollments
    }
    return context

#Na inclusion_tag um .html é forçado. Recomendada quando o .html a ser redereizado é mais complexo  possuindo muitas váriáveis a serem tratadaas, no exemplo atual apenas uma variável é trabalhada assim o simple_tag foi mais indicado
#Na simple_tag o valor é retornado ao uma várial e a mesma pode ser utilziado de qualquer forma, assim o código fica mais flexível pois a mesma tag pode ser usada em outr ponto com outro comportamento

@register.simple_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)