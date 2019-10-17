#### docker
docker run -d -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=123 postgres

docker ps --all

### django

django-admin startproject mysite

django-admin startapp companies

python manage.py runserver

#### migrations
python manage.py makemigrations <app>

python manage.py migrate

заполнение полей
python manage.py loaddata companies/fixtures/initial_fixture.yaml

#### Что можно улучшить:

1. Есть кейс, когда модели могут лежать в отдельной папке типа "models".
Можно научить брать оттуда.
https://stackoverflow.com/questions/5534206/how-do-i-separate-my-models-out-in-django
Также по аналогии с url

2. Авторизация. Проверить как будет работать с авторизацией. Могут быть дополнительные правки для поддержки авторизации.
(CsrfViewMiddleware)

3. Можно сделать с https://www.django-rest-framework.org/. Вставив в settings.py как зависимость и используя уже готовые компоненты.

4. Должности через enum (как кроме choise)

5. Multi-Column Sort
ORDER BY Last_Modified DESC, Email ASC

6. Усилить валидацию (проверка на лишние параметры, проверка, что присутствуют только поля, допустимые для модели)

#### todo: remove not needed from settings.py