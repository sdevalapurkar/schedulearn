from django.shortcuts import render, HttpResponse

def load_404(request, exception):
    return render(request, 'errors/404.html')
