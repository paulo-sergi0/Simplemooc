from django import forms
from django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template

from .models import Coment

class ContactCourse(forms.Form):
    
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Messagem/Dúvida', widget=forms.Textarea)
    #Se algum dos campos não for obrigatório o parâmetro "required=False" deve ser passado

    def send_mail(self, course):
        subject = '[%s] Contato' % course
        #message = 'Nome: %(name)s; Email: %(email)s; Mensagem: %(message)s'
        ##message = 'Nome: %s; Email: %s; Mensagem: %s' #Forma sem nomeação é passada uma lista. Com nomeação (linha acima) é passado um dicionário
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        #message = message % context
        #send_mail(
        #    subject, message, settings.DEFAULT_FROM_EMAIL,
        #    [settings.CONTACT_EMAIL]
        #)
        template_name = 'courses/contact_email.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Coment
        fields = ['comment']
