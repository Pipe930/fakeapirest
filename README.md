## Fake Api Rest 

This is a project of a Fake REST API for products, users, and posts so that anyone can use it and develop their frontend projects.

## Tecnologies

- Python 3.12.4
- Django 5.0.6
- Rest Framework 3.15.1
- Mysql 8.0

## Local Environment

First, we need to clone the project into your environment:

```bash
git clone https://github.com/Pipe930/fakeapirest.git
cd ./fakeapirest
```

Now that we have cloned the repository, we need to create a Python virtual environment for the installation of the project's dependencies:

```bash
python -m venv env
virtualenv env

# Windows
env\Scripts\activate

# Linux o Mac
source env/bin/activate
```

> [!NOTE]
> If you want to use virtualenv, you need to install it with pip `pip install virtualenv`.

### Install Dependences

With the Python virtual environment activated and configured, we install the project dependencies:

    pip install -r requirements.txt

### Environment Variables

Now we need to configure the environment variables. In the project folder, I left a `.env.example` file as an example of the environment variables that need to be used:

```bash
SECRET_KEY='secret-key'
SIMPLE_JWT_SIGNING_KEY='key-jwt'

DATABASE_NAME='namedatabase'
DATABASE_USER='root'
DATABASE_PASSWORD='password'
DATABASE_HOST='localhost'
DATABASE_PORT=3306
```

> [!NOTE]
> For the `SECRET_KEY` environment variable, you need to enter a valid secret key for the project to run. You can obtain a key from the following page **[Djecrety](https://djecrety.ir/)**.

### Migrations

With the environment variables configured, we need to run the model migrations to create the tables in the database:

> [!IMPORTANT]
> Before performing the migrations, we need to create a series of folders within each app of the project. That is, inside the `apps` folder are the applications, and within each application, you need to create a `migrations` folder with a file inside this folder named `__init__.py`. This will allow Django to recognize the models and generate the migration files.

```bash
python manage.py makemigrations
python manage.py migrate
```

This will migrate the models to the database and create the corresponding tables for the application's operation.

### Create Superuser (optional)

This section is optional and not mandatory. To create a superuser for the application, you need to run the following command:

    python manage.py createsuperuser

### Data Insertion

I've created a small script to provide the API with some default data. This data comes from another API called **[DummyJSON](https://dummyjson.com/)**, which you can use for your frontend projects. To insert the data into the database, you need to run the following command:

    python manage.py fetch_and_insert

### Execution

With everything ready and configured, let's run the project with the following command:

    python manage.py runserver

Done! If everything went well, you now have the project running locally on your computer.

## Docker Enviroment

To run the project in a Docker environment, we need to have configured the environment variables using the example file I attached to the project, `.env.example`, as mentioned in one of the previous steps.

*I will assume that you already have Docker installed on your computer*.

### Image Create

Now that we have the environment variables configured, let's create the Docker image for the project:

    docker compose build

### Execution

With the Docker image created, we will run the project through Docker:

    docker compose up

## Testing

A couple of unit tests were developed for each application, and each view underwent a unit test to verify the functionality of the endpoint and to ensure that there are no modifications causing errors in other functionalities of the API. To run the tests, you need to enter the following command:

    python manage.py test

All the unit tests located within the `tests` file, where all the test files are, will be executed.

