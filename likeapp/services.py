from likeapp import models
from django.db.models import Count


def get_path_upload_file(instance, filename):
    # file will be uploaded to media/photo/user_<id>/<filename>
    return f'photo/user_{instance.account.user.id}/{filename}'
