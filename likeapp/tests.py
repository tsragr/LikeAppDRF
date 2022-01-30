from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from likeapp import models
from account.models import Account
import io
from PIL import Image

client = APIClient()


class CreateImageTest(TestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Maxim', password='123qwe')
        self.account = Account.objects.create(user=self.user, bio='test')

    def test_post_image(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.post('/image/img/', {'account': self.account, 'image': self.generate_photo_file()})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Image.objects.all().count(), 1)

    def tearDown(self) -> None:
        User.objects.all().delete()
        Account.objects.all().delete()
