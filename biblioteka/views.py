from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Witaj na stronie Baza druków krakowskich!")
# Create your views here.
