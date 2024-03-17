from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def Face_rec(request):
    return render(request, 'face_rec.html')