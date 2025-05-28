from django.test import TestCase
from .models import CustomUser

# Create your tests here.
class UserModelTest(TestCase):

    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.password = 'test1234'
        self.user = CustomUser.objects.create(name=self.name, email=self.email, password=self.password)

    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)