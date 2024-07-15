from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('runcalc/', views.run_maincalc),
]