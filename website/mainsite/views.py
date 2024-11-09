# main/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'mainsite/index.html')  # or whatever your template path is