from django.urls import path

from ..views import city_view

urlpatterns = [
    # todo: можно сделать лучше через регулярные выражения
    # всё в 1 вызове с проверкой на валидность параметров
    # https://docs.djangoproject.com/en/2.2/topics/http/urls/
    path('city', city_view.city),
    path('city/<int:city_id>', city_view.city),
]
