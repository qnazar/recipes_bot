from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_list, name='users'),
    path('add_recipe/', views.add_recipe, name='add_recipe')
]
