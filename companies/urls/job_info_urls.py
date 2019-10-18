from django.urls import path

from ..views import job_info_view

urlpatterns = [
    # todo: можно сделать лучше через регулярные выражения
    # всё в 1 вызове с проверкой на валидность параметров
    # https://docs.djangoproject.com/en/2.2/topics/http/urls/
    path('job_info', job_info_view.job_info),
    path('job_info/<int:job_info_id>', job_info_view.job_info),
]
