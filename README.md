# Microservicios

### Local Setup


### 1 Run with docker
    $ docker-compose build
    $ docker-compose up

### 2 Initial migration
    $ docker-compose exec places python manage.py recreate_db
    $ docker-compose exec peoples python manage.py recreate_db

### 3 Populate data in databases
    $ docker-compose exec places python manage.py populate_db
    $ docker-compose exec peoples python manage.py populate_db

### RUN Tests
    $ docker-compose exec places python manage.py test
    $ docker-compose exec peoples python manage.py test

### Run flake8
    $ docker-compose run --rm places flake8
    $ docker-compose run --rm peoples flake8

### Services
Service name| Service endpoint|
-------|---|
places|http://localhost:8081/v1/places/
peoples|http://localhost:8082/v1/peoples/
got|http://localhost:8083/v1/got/places/
swagger|http://localhost:8084/
