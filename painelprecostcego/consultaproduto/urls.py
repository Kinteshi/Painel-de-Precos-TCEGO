from django.urls import path
from consultaproduto import views

app_name = 'consultaproduto'

urlpatterns = [
    path('', views.index, name='index'),
    path('consulta/', views.consulta, name='consulta'),
]
