from django.shortcuts import render

# Create your views here.

def mruandsru(request):
    # render the existing template
    return render(request, 'mruandsru.html')

def bscaboutus(request):
    return render(request, 'bscaboutus.html')

def index(request):
    return render(request, 'index.html')
