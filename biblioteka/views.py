from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def informacje(request):
    return render(request, 'informacje.html')

