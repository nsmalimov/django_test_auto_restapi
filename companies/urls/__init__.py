from django.urls import include, path

urlpatterns = [

    path('', include('companies.urls.person_urls')), 
    path('', include('companies.urls.city_urls')),
    path('', include('companies.urls.job_info_urls')),
]