# Mauritius Renal registry app

This is a Django application to capture data for renal patients in Mauritius.


## Developer notes

### Creating migrations

If you make changes to the models in `renaldataregistry`, make sure to create migrations and check them into source control.

Create migrations with `python src/manage.py makemigrations`.

Migrations will be applied automatically when the application container starts. If you're running outside of a container, run migrations manually (see Getting Started below).

### Building Docker image

### Deploying Docker image

#### Environment variables

#### Superuser creation

## Getting Started

These instructions will get you a copy of the project to run it on your local machine.

### Prerequisites

python3

### Installing

1. Clone the project.

```
git clone project-url
cd project-directory
```

2. Create and activate virtualenv.

```
python3 -m venv venv
source ./venv/bin/activate # (on windows: venv\Scripts\activate)
```

3. Install requirements.

```
pip install -r requirements.txt
```

4. Edit database settings (name, user and password)

```
edit mauritiusrenalregistry/settings.py section DATABASES
```

5. Run migrations.

```
python src/manage.py migrate
```

6. Create super user.

```
python src/manage.py createsuperuser
```

7. Run dev server.

```
python src/manage.py runserver
```

Open [localhost](http://localhost:8000) in the browser on port 8000 and login with the super user credentials.
