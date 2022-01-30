from likeapp import models
from rest_framework import serializers
from django.db.models import Count


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Image's serializer
    """
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Image
        fields = ('image', 'likes_count')

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeImageSerializer(serializers.ModelSerializer):
    """
    Image's like serializer
    """
    class Meta:
        model = models.Like
        fields = "__all__"


class ImagesViewedSerializer(serializers.ModelSerializer):
    """
    Serializer images viewed by user
    """
    class Meta:
        model = models.ImagesViewed
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    """
    Image's reports serializer
    """
    class Meta:
        model = models.Report
        fields = ('text',)
