from django.shortcuts import render

def home(request):
    return render(request, 'biblioteka/home.html')

def info(request):
    return render(request, 'biblioteka/info.html')


