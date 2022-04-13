# Mauritius Renal registry app

This is a Django application to capture data for renal patients in Mauritius.


## Developer notes

### Creating migrations

If you make changes to the models in `renaldataregistry`, make sure to create migrations and check them into source control.

Create migrations with `python src/manage.py makemigrations`.

Migrations will be applied automatically when the application container starts. If you're running outside of a container, run migrations manually (see Getting Started below).

### Building Docker image

Docker images are automatically built by GitHub Actions, and published to https://github.com/renalreg/mauritius-renaldataregistry/pkgs/container/mauritius-renaldataregistry.

You can reference images by various tags:

- Tagged releases will create a new version-tagged image.
  - E.g. A GitHub release `v1.0.0` will create an image tagged `1.0.0`
- Pushing to any branch will create a branch-tagged image
  - E.g. pushing to `main` will update the image tagged `main`

### Deploying Docker image

To deploy the container:

1. Clone this repository to your server
2. Create a populated `.env` file in the root of the repository
3. Run `docker-compose up` (or `docker-compose up -d` to run in the background)

The application will be running on port 8000, so set up your reverse proxy to redirect requests to that port.

The docker-compose file is set up to also serve collected static files, so no downstream configuration is required for static files.

### Updating deployed Docker image

1. Update the repository on your server (e.g. `git pull`)
2. Rebuild the Docker image with `docker-compose build`
3. Restart the container with the updated image using `docker-compose down && docker-compose up -d`

### Accessing logs

1. Navigate to the application repository on your server
2. `docker-compose logs` will show the logs of the container.

#### Environment variables

Example `.env` file structure:

```ini
ALLOWED_HOSTS="renaldata1.exampledomain.com,renaldata2.exampledomain.com"
DEBUG=0

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=changeme
DJANGO_SUPERUSER_EMAIL=admin@email.com

```

Note: Once the container has started for the first time, you can remove `DJANGO_SUPERUSER_` items from `.env`. They exist only to create the initial superuser account on first-run.

Leaving them in the file won't do any damage, since Django won't create a new user if the username already exists, it's just cleaner to remove it. Doing so will result in an output line `CommandError: You must use --username with --noinput.` which can be safely ignored.

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
