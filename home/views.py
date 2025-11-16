from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    
    peoples = [
        {'name': 'Rohit', 'age': 5},
        {'name': 'Sahil', 'age': 25},
        {'name': 'Ankit', 'age': 26},
        {'name': 'Anshul', 'age': 27},
        {'name': 'Rishabh', 'age': 28},
    ] 
    for people in peoples:
        print(people['age'])
        print('yes')
    vegetables = ['Potato', 'Tomato', 'Cabbage', 'Cauliflower', 'Brinjal']
    return render(request, 'home/index.html', context={'pages': 'Django 2025','peoples': peoples, 'vegetables': vegetables})



def about(request):
    context = {"page": "about"}
    return render(request, 'home/about.html', context) 

def contact(request):
    context = {"page": "contact"}
    return render(request, 'home/contact.html', context) 

def success_page(request):
    print('*'*50)
    return HttpResponse('<h1>Hey this is a success</h1>')

def index(request):
    return render(request, 'index.html')