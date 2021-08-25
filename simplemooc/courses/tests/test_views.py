from django.conf import settings
from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse

from simplemooc.courses.models import Course

class ContactCourseTestCase(TestCase):

    #Sempre que algum teste for chamado esse método deve executado antes
    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')

    #Sempre que algum teste for chamado esse método deve executado depois
    def tearDown(self):
        self.course.delete()

    def test_contact_form_error(self):
        data = {'name':'Fulano de Tal', 'email':'', 'message':''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório')

    def test_contact_form_sucess(self):
        data = {'name':'Fulano de Tal', 'email':'tetse@teste.com', 'message':'olá'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        #Verficando a quantidade de mensagens atráves do outbox, testando se a quantidade é igual a 1
        self.assertEqual(len(mail.outbox),1)
        #Verficando se o destinatário é o e=mail setado nas settings atráves do outbox[0].to
        #Outras opções são outbox[0].subject, outbox[0].body ...
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])