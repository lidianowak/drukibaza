from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'biblioteka/home.html')

def info(request):
    return render(request, 'biblioteka/info.html')


