## Setup Project

### Setup & activate virtual environment
```
python -m venv venv

source venv/scripts/activate
```

### Install django
```
pip install django
```

### Optional: Upgrade pip
```
python.exe -m pip install --upgrade pip
```

### Create a django project
```
django-admin startproject <myproject> .
```

### Add an app to the project settings
```
python manage.py startapp <myapp>
```

## Step 1: Create Failing TDD Test

### In settings.py, add your installed app

- myproject/settings.py

- Add <myapp> under [INSTALLED APPS] 

- Write the test in myapp/tests.py

```
from django.test import TestCase

# Create your tests here.
class UserModelTest(TestCase):

    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.user = ''

    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
```

### Create the model's skeleton
- In <myapp>/models.py, create model's skeleton

```
from django.db import models

# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=30)
```

### Refractor the test

```
#tests.py
# Change this line
self.user = CustomUser()
```

### Create class object with test data

```
# tests.py
self.user = CustomUser.objects.create(name=self.name)
```

### Apply migrations
```
python manage.py migrate
```

### Run the TDD test
```
python manage.py test
```

## Step 2: Refractor the code

---

# API Documentation

API Documentation Setup with drf-yasg in Django

This guide explains how to generate interactive API documentation for a Django REST Framework project using drf-yasg.

## Prerequisites
- Python & Django installed
- Django REST Framework (`djangorestframework`) installed
- Your Django project and apps are already set up

### Step 1: Install drf-yasg

Run the following command:
```bash
pip install drf-yasg
```

### Step 2: Add to `INSTALLED_APPS`

In your `settings.py`, add:
```python
INSTALLED_APPS = [
    # other apps
    'rest_framework',
    'drf_yasg',
]
```

### Step 3: Configure URLs

In your main `urls.py` (e.g., `configs/urls.py`), add:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Description of your API",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),  # Include your app URLs here

    # API documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### Step 4: Define API Views and Serializers
- Make sure your Django app (`your_app`) has views and serializers defined using Django REST Framework.
- drf-yasg uses these to generate the API documentation.

### Step 5: Run the Development Server

Run the server with:
```bash
python manage.py runserver
```

### Step 6: Access the API Documentation

Open your browser and visit:
- Swagger UI: http://localhost:8000/swagger/
- Redoc UI: http://localhost:8000/redoc/
- http://localhost:8000/api/users/

#### Additional Notes
- drf-yasg auto-generates docs from your serializers, views, and URL patterns.
- You can customize the schema info and permissions as needed.
- For production, use a proper WSGI/ASGI server; the Django dev server is only for development.

#### References
- [drf-yasg GitHub](https://github.com/axnsan12/drf-yasg)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Redoc](https://github.com/Redocly/redoc)

```
tdd-project/          # Project root folder
 ├─ configs/          # Project configs: settings.py, urls.py, wsgi.py, asgi.py
 ├─ users/            # App folder: models.py, views.py, urls.py, serializers.py, ...
 ├─ manage.py         # Django management tool
```


