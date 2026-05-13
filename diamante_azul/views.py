
from django.shortcuts import render

def home(request):
    return render(request, 'home/landing.html')


# ! ERROR 404
def error_404_view(request, exception):
    return render(request, '404.html', status=404)

# ! ERROR 500
def error_500_view(request):
    return render(request, '500.html', status=500)