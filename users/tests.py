from django.test import TestCase
from .models import CustomUser

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = 'test'
        cls.email = 'test@example.com'
        cls.password = 'test1234'
        cls.user = CustomUser.objects.create(
            name=cls.name,
            email=cls.email,
            password=cls.password
        )

    def test_user_creation(self):
        self.assertEqual(self.user.name, self.name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password, self.password)
