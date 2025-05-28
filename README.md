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

