from django.shortcuts import render

def home(request):
    return render(request, 'biblioteka/home.html')

def baza(request):
    return render(request, 'biblioteka/baza.html')  # lub inny szablon

def info(request):
    return render(request, 'biblioteka/info.html')  # jeśli potrzebne
