from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    #Primeiro parâmtro: Toda view do Django recebe como primeiro parâmetro o request
    #Segundo parâmetro: Nome do templeate que deve ser exibido
    #Terceiro parâmetro: é o contexto, um dict
    #Obs: Por padrão o Djando reconhece templates que estiverem dentro da pasta templates do projeto
    #Obs: o retorno de uma view sempre deve ser um HttpResponse, a função render retorna um HttpResponse
#    return render(request, 'home.html', {'usuario':'Paulo'}) 
    return render(request, 'home.html') 

def contact(request):
    return render(request, 'contact.html')