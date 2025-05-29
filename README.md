# Django TDD Tutorial - Complete Guide

## 1. Setup Project

1.1 Setup & activate virtual environment
```bash
python -m venv venv
source venv/scripts/activate  # On Windows: venv\Scripts\activate
```

1.2 Install django
```bash
pip install django
```

1.3 Optional: Upgrade pip
```bash
python.exe -m pip install --upgrade pip
```

1.4 Create a django project
```bash
django-admin startproject myproject .
```

1.5 Add an app to the project
```bash
python manage.py startapp myapp
```

1.6 Add app to settings

Open myproject/settings.py

Add 'myapp' under INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Add this line
]
```

##  2. Step 1: Create Failing TDD Test (RED 🔴)
   
2.1 Write the first failing test

In myapp/tests.py:
```python
from django.test import TestCase
from .models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.user = ''  # This will cause test to fail
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
```

2.2 Create empty model skeleton
In myapp/models.py:
```python
from django.db import models

# Empty model - will cause import error
class CustomUser(models.Model):
    pass
```

2.3 Run test (should fail)
```bash
python manage.py test
```

Expected: Test fails because model has no fields


##  3. Step 2: Make Test Pass (GREEN 🟢)
   
3.1 Add minimal model fields
   
In myapp/models.py:
```python
from django.db import models

class CustomUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=128)
```

3.2 Update test to create user object

In myapp/tests.py:
```python
from django.test import TestCase
from .models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        # Create actual user object
        self.user = CustomUser.objects.create(
            name=self.name,
            email=self.email,
            password=self.password
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
```

3.3 Create and apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

3.4 Run test (should pass)
```bash
python manage.py test
```

Expected: Test passes ✅

##  4. Step 3: Refactor Code (REFACTOR 🔵)
   
4.1 Add validation and constraints
In myapp/models.py:
```python
from django.db import models

class CustomUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)  # Add unique constraint
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
```

4.2 Update migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

4.3 Run test (should still pass)
```bash
python manage.py test
```

##  5. Step 4: Add New Failing Test (RED 🔴)
   
5.1 Add email uniqueness test

In myapp/tests.py:
```python
from django.test import TestCase
from django.db import IntegrityError
from .models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.user = CustomUser.objects.create(
            name=self.name,
            email=self.email,
            password=self.password
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
    
    # New failing test
    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                name='test2',
                email=self.email,  # Duplicate email
                password='password2'
            )
```

5.2 Run test
```bash
python manage.py test
```
Expected: New test should pass because we already added unique=True

##  6. Step 5: Add Password Security Test (RED 🔴)

6.1 Add password hashing test

In myapp/tests.py:

```python
from django.test import TestCase
from django.db import IntegrityError
from .models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.user = CustomUser.objects.create(
            name=self.name,
            email=self.email,
            password=self.password
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
    
    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                name='test2',
                email=self.email,
                password='password2'
            )
    
    # New failing test - password should be hashed
    def test_password_is_hashed(self):
        self.assertNotEqual(self.user.password, self.password)
        self.assertTrue(self.user.password.startswith('pbkdf2_sha256$'))
```

6.2 Run test (should fail)
```bash
python manage.py test
```
Expected: Password test fails because we store plain text

## 7. Step 6: Implement Proper Authentication (GREEN 🟢)
   
7.1 Use Django's built-in authentication

In myapp/models.py:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.email})"
```

7.2 Add to settings.py

Add this line to myproject/settings.py:

```python
AUTH_USER_MODEL = 'myapp.CustomUser'
```

7.3 Update tests to use create_user

In myapp/tests.py:

```python
from django.test import TestCase
from django.db import IntegrityError
from .models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.username = 'testuser'
        # Use create_user for proper password hashing
        self.user = CustomUser.objects.create_user(
            username=self.username,
            name=self.name,
            email=self.email,
            password=self.password
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.username, self.username)
    
    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username='testuser2',
                name='test2',
                email=self.email,  # Duplicate email
                password='password2'
            )
    
    def test_password_is_hashed(self):
        # Password should be hashed, not plain text
        self.assertNotEqual(self.user.password, self.password)
        self.assertTrue(self.user.password.startswith('pbkdf2_sha256$'))
    
    def test_password_verification(self):
        # Should verify correct password
        self.assertTrue(self.user.check_password(self.password))
        # Should reject wrong password
        self.assertFalse(self.user.check_password('wrongpassword'))
```

7.4 Reset database (due to AUTH_USER_MODEL change)

```bash
rm db.sqlite3
rm myapp/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

7.5 Run tests (should all pass)

```bash
python manage.py test
```

## 8. Step 7: Add Authentication Test (RED → GREEN)
   
8.1 Add authentication test

In myapp/tests.py, add:

```python
from django.contrib.auth import authenticate

# Add this test method to your class
def test_authentication(self):
    # Should authenticate with email and password
    user = authenticate(username=self.email, password=self.password)
    self.assertEqual(user, self.user)
    
    # Should not authenticate with wrong password
    user = authenticate(username=self.email, password='wrong')
    self.assertIsNone(user)
```

8.2 Run final tests

```bash
python manage.py test
```

## 9. TDD Cycle Summary
    
Red 🔴 (Write Failing Test)

Write test that describes desired behavior
Test fails because feature doesn't exist
This defines what you need to build

Green 🟢 (Make Test Pass)

Write minimal code to make test pass
Don't worry about perfect code yet
Focus on making the test pass

Refactor 🔵 (Improve Code)

Clean up code while keeping tests passing
Add validation, better structure
Tests ensure you don't break anything

Repeat

Add new failing test for next feature
Continue the cycle
Build features incrementally

## 10. Benefits of This Approach

✅ No over-engineering: Only build what tests require
✅ Immediate feedback: Know instantly if something breaks
✅ Better design: Tests force you to think about interfaces
✅ Confidence: Refactor without fear of breaking things
✅ Documentation: Tests serve as living documentation

## 11. Next Steps

Try adding more tests for:

User roles/permissions
Email validation
Password strength requirements
User profile information
Account activation

Remember: Red → Green → Refactor → Repeat 🔄

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
