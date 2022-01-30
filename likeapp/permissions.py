from rest_framework.permissions import BasePermission
from likeapp.models import Image
from django.db.models import Count


class CanPostOrBan(BasePermission):
    """
    Permission prohibit to post images when you have >= 5 images with >= 10 reports
    """

    def has_permission(self, request, view):
        return not Image.objects.filter(account__user=request.user).alias(Count('reports')).filter(
            reports__count__gte=10).count() >= 5
