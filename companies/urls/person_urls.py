from django.urls import path

from ..views import person_view

urlpatterns = [
    # todo: можно сделать лучше через регулярные выражения
    # всё в 1 вызове с проверкой на валидность параметров
    # https://docs.djangoproject.com/en/2.2/topics/http/urls/
    path('person', person_view.person),
    path('person/<int:person_id>', person_view.person),
]
