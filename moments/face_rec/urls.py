from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('face_rec', views.Face_rec, name='face_rec')
]
