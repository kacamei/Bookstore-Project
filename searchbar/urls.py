from django.urls import path

from searchbar import views

urlpatterns = [
    path('',views.secondTry, name='secondTry'),
    
]
