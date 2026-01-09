from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('', views.index, name='index'),
    path('setvalues/', views.setvalues, name='setvalues'),
    path('spin/', views.spin_number, name='spin'),
]
