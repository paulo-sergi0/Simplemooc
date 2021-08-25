from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):

    # Método pesquisa o parâmetro informado dentro do name e da description
    # "," entre os parâmetros é um and: Ira retornar somentos os registros que possuirem o parâmetro passado tanto no nome quanto na descrição
    # Para utilzar o "ou" é nescessário utilizar a class "Q" que está dentro do models
        # Dentro do "Q":
            # "&" e "," para and
            # "|" para or
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query))


class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    start_date = models.DateField('Data de Incío', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    #Método sobreescrito para mostrar o nome do curso no painel "admin" do Django
    def __str__(self):
        return self.name

    def release_lessons(self):
        today = timezone.now().date()
        # __gte = Maior ou igual (para mais informações pesquisar sobre django low caps)
        return self.lessons.filter(release_date__lte=today)

    #Decorator  que utiliza o método reverse (from django.core.urlresolvers import reverse) para regatar uma URL dado um nome
    #@models.permalink  #Esse decorator foi depreciado no Djanfo 2.0, portanto o get_absolute_url foi comentado (por ter comentado a opção "ver  no site" no painal Admin não é mais exibida)
    #ToDO: Descomentar o get_absolute_url e corrigir a exbição do link "ver no site"
   # def get_absolute_url(self):
   #     return ('courses:details', (), {'slug': self.slug})
        #O retorno desse método é uma tupla com as seguintes parâmetros
        #1 ('courses:details') : URL (namespace = courses e valor = details)
        #2 () : Argumentos não nomeados (que não está sendo utilizado no momento)
        #3 {'slug': self.slug} : Argumentos nomeaveis (um dictonary)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name'] # '-name' seria a order descrescente


class Lesson(models.Model):

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de Liberação', blank=True, null=True) #Campo de controle interno não ira ser exibido ao usuário

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)

    create_at = models.DateTimeField('Criado em', auto_now_add=True) 
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    #Para verificar se uma determinada aula está disponível
    def is_available(self):
        if self.release_date:
            #Poderia ser feito utilizando o import "datetime" porém é ficará sucetivél a erros de "zona horária" pois "datetime" usa o horário da máquina local
            today = timezone.now().date()            
            return self.release_date <= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']        


class Material(models.Model):
    
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessions/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials', on_delete=models.CASCADE)

    def is_embedded(self):
        return bool(self.embedded)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Matérial'
        verbose_name_plural = 'Materiais'


class Enrollment(models.Model):

    #Tupla de tuplas
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    #Similar a implementação do model accounts
        #Serve para criar uma forekey para o usuário. settings.AUTH_USER_MODEL é para usar o usuário "padrão" atual (pois o usuário padrão do Django foi sovbreescrito)
    #related_name serve é um atributo que será criado no usuário para efetuar uma busca nesse model "filho" (Enrollment) pelo o usuário em questão, faz a relação com esse usuário - Mais detalhes verificar model accounts
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        on_delete = models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso', on_delete = models.CASCADE,
        related_name='enrollments'
    )
    #Como o primeiro parâmetro é o verbose name o termo "verbose_name" foi omitido, porém poderia ser incluído sem problemas (parâmetro nomeado)
    #No django os tipos inteiro, charfield (dentre outros) eles possuem uma opção de "choices". Choices é um conjunto predeterminado de opções possíveis que o próprio djando já faz a integração com o sistema de formulários (incluíndo validações e outros procedimentos)
    status = models.IntegerField('Situação', 
        choices=STATUS_CHOICES, default=0, blank=True
    )
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Incrições"
        #uma tupla de tuplas, para cada tupla deve ser indicado 2 ou mais campos
            #São indices de unicidade. Indica que deve ser criado a nível de banco de dados um indice de unicidade para usuário e curso. Serve para evitar duplicidade pois não será possível cadastrar o mesmo usuário no mesmo curso.
        unique_together = (('user', 'course'),)

class Announcement(models.Model):
    
    course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')
    create_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-create_at'] #Descrescente "-"

class Coment(models.Model):

    announcement=models.ForeignKey(Announcement, 
        on_delete=models.CASCADE,
        verbose_name='Anúncio',
        related_name='comments') #Caso related_name não fosse difinido seria necessáira a implementação do código para recuperação dos comentários do anuncio, gerando uma maior complexidade para a model/view (já que não seria possível fazer no template). Caso não setado poderia ser acessado atraves de "coment_set"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='usuário')
    comment = models.TextField('Comentário')
    create_at = models.DateTimeField('Criado em', auto_now_add=True) #Um model poderia ser criado e heradado para evitar repetir o código desses campos específicos
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name='Comentário'
        verbose_name_plural='Comentários'
        ordering=['create_at']

"""
    método para utilizar o "signal" do evento pos_save (presente nas classes que herfa, de "Model"). 
        Só será necessário o uso dos parâmetros instance e created, porém como não são os unicos é necessário utilzar o **kwargs
"""
def post_save_announcement(instance, created, **kwargs):
    if created: #para enviar o e-mail apenas quando o anuncio for criado (e não sempre que for atualizado)
        subject = instance.title
        context = {
            'announcement':instance
        }
        template_name = 'courses/announcements_mail.html'
        enrollements = Enrollment.objects.filter(
            course=instance.course, status=1
        )
        for enrollement in enrollements:#Laço incluído para não não lançar apenas um e-mail para todos os usuários(que poderia ser feito passando a lista dos e-mails, porém os e-mails ficaram em copia(do e-mail)).
            recipient_list = [enrollement.user.email]
            send_mail_template(subject, template_name, context, recipient_list) 

#Definição de qual método (post_save_announcement,) será utilizado quando o sender (o alvo for executado)
models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement' #parâmetro para evitar que se reproduza outro signal com o mesmo método
)