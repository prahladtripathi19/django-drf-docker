# django-drf-docker
Django DRF with docker 

Step-1:
Create a docker file and add requirements. Please see the Dockerfile
Create app folder

Step-2: Run comman
docker build .

Step-3: Create docker-compose.yml file. Please check the file for for configurations

Step-4: Run 
docker-compose build

This will create a docker image and named the tag projectname-app:latest

Step-5: Create django project
docker-compose run app sh -c "django-admin startproject app ."

Step-6: run test case
docker-compose run app sh -c "python manage.py test"

Step-7: clear container and 
docker-compose run --rm app sh -c "python manage.py startapp user"

