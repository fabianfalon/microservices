# Microservicios
Ejemplo de microservicios en flask y conexion entre los mismos.

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

### Run Tests
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
swagger (places, peoples, got)|http://localhost:8084/
users|_http://localhost:8085/users/v1/users_
swagger-users|http://localhost:8085/users/v1/ui/
authentication|http://localhost:8086/auth/v1/
swagger-authentication|http://localhost:8086/auth/v1/ui/
