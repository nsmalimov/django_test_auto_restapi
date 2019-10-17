from django.urls import path

from . import views

urlpatterns = [
    # todo: можно сделать лучше через регулярные выражения
    # всё в 1 вызове с проверкой на валидность параметров
    # https://docs.djangoproject.com/en/2.2/topics/http/urls/
    path('person', views.person),
    path('person/<int:person_id>', views.person),
]
