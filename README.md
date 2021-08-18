# Mauritius Renal registry app

This is a Django application to capture data for renal patients in Mauritius.

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
python manage.py migrate
```

6. Create super user.

```
python manage.py createsuperuser
```

7. Run dev server.

```
python manage.py runserver
```

Open [localhost](http://localhost:8000) in the browser on port 8000 and login with the super user credentials.
