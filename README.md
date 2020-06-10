# Microservicios
Ejemplo de microservicios en flask y conexión entre los mismos.

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

### Run migrations
    $ docker-compose exec users python main.py db migrate
    $ docker-compose exec users python main.py db upgrade

### Services
Service name| Service endpoint|
-------|---|
places|http://localhost:8081/v1/places/
peoples|http://localhost:8082/v1/peoples/
got|http://localhost:8083/v1/got/places/
swagger (places, peoples, got)|http://localhost:8084/
users|http://localhost:8085/users/v1/users/
swagger-users|http://localhost:8085/users/v1/ui/
authentication|http://localhost:8086/auth/v1/
swagger-authentication|http://localhost:8086/auth/v1/ui/


#### RUN with kubernetes
    $ minikube start
    $ cd k8s
    $ kubectl -f apply .

#### get minikube ip to access
    $ minikube ip

Service name| Service endpoint with minikube ip|
-------|---|
got|http://192.168.99.100:31000/v1/got/places/
places|http://192.168.99.100:31020/v1/places/
peoples|http://192.168.99.100:31050/v1/peoples/
authentication|http://192.168.99.100:31080/auth/v1/
swagger-authentication|http://192.168.99.100:31080/auth/v1/ui/
users|http://192.168.99.100:31090/users/v1/users/
swagger-users|http://192.168.99.100:31090/users/v1/ui/

#### push to docker hub
    $ docker login
    $ docker build -t fabianfalon/authentication-service:tag .
    $ docker push fabianfalon/authentication-service:tag