Это тестовый django-проект для отладки плагина https://github.com/nsmalimov/auto_restapi_django_plugin, который 
уже скопирован в проект и применён к нему.

Для тестирования создал модели и фикстуры для заполнения таблиц тестовыми данными. 

### docker
Для поднятия локальной базы PSQL можно использовать docker-образ.

`docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=123 postgres`

`docker ps --all`

Не забудьте создать базу данных "django_test_auto_restapi" (см. settings.py).

### django

`django-admin startproject mysite`

`django-admin startapp companies`

`python manage.py runserver`

### migrations
`python manage.py makemigrations <app>`

`python manage.py migrate`

Заполнение полей:
`python manage.py loaddata companies/fixtures/initial_fixture.yaml`

#### TODO:

1. Должности в модели Person через enum (как кроме choise). Проверить, что choise - работает.
2. Удалить лишнее из settings.py, так как проект тестовый, небходимости в некоторых полях нет.