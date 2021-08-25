#from django.http import response
from django.test import TestCase
from django.core import mail
#from django.test import client
from django.test.client import Client #Simula o navagador 
from django.urls import reverse

'''
    Por padrão o django irá buscar métodos com o préfixo "test" para execução dos testes
    Cada método é um teste (em um método podem exitir vários "assert")
'''

class HomeViewTest(TestCase):

    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core:home'))
        #Na documentação do Django estão disponíveis os outros "asserts"
        self.assertAlmostEqual(response.status_code, 200)
    
    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        #assertTemplateUsed confirma os templates utilizados. Retorn positivo para home e base, pois home herda de base
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')
         
