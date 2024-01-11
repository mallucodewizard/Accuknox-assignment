#### HOW TO ?
Follow these instructions to run this project locally

- Make sure you installed **Docker** and **docker-compose** in your local machine; If not please follow the links to do the same.
    
    - [Docker installation guide](https://docs.docker.com/engine/installation/) <br>
    - [Docker-compose installation guide](https://docs.docker.com/compose/install/)


- Clone the project to local machine
- project directory
 ``` 
 cd socail_backen
  ``` 
- Run following command in command line
    ``` 
    docker-compose up -d --build
    ```
- Run or Make migrations
``` 
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
``` 

- Create a superuser
    docker-compose exec web python manage.py createsuperuser
<!-- - Run containers in terminal if needed
    docker-compose up -d   -->
- Seed sample data

    docker-compose exec web python manage.py seed_data
