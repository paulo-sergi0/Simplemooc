from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course

#Exemplos de testes utilizando a app mommy(gera os objetos com dados aleatórios, dispensando o tempo de criação e preenchimento dos dados dos testes)
class CourseManagerTestCase(TestCase):

    def setUp(self):
        #Criação de 5 cursos de nome Python na Web com Django e o resto dos campos com valores aleatórios
        self.courses_django = mommy.make(
            'courses.Course', name='Python na Web com Django', _quantity=5
        )
        self.courses_dev = mommy.make(
            'courses.Course', name='Python para Devs', _quantity=10
        )
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()
    
    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search),5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search),10)
        search = Course.objects.search('python')
        self.assertEqual(len(search),15)