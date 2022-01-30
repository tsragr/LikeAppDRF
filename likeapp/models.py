from django.db import models
from account.models import Account
from likeapp.services import get_path_upload_file


class Image(models.Model):
    """
    Image's model
    """
    image = models.ImageField(upload_to=get_path_upload_file)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.image}"


class Like(models.Model):
    """
    Image's like model
    """
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.image.image} {self.user.user.username}"


class Report(models.Model):
    """
    Image's report model
    """
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='reports')
    text = models.TextField()

    def __str__(self):
        return f"{self.image.image} {self.user.user.username}"


class ImagesViewed(models.Model):
    """
    Model images viewed by user
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='viewed_images')
    images = models.ManyToManyField(Image, related_name='images_viewed_by_user')

    def __str__(self):
        return f"{self.user}"
