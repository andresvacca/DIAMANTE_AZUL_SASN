
from django.shortcuts import render

def home(request):
    return render(request, 'home/landing.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)