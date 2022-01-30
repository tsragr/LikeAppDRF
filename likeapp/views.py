from django.shortcuts import render
from rest_framework import viewsets, mixins
from likeapp import serializers
from likeapp import models
from account.models import Account
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from likeapp.permissions import CanPostOrBan
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response


class ImageRetrieveCreateViewSet(viewsets.GenericViewSet,
                                 mixins.CreateModelMixin,
                                 mixins.ListModelMixin):
    """
    View for create, get, like, report and viewed images
    """

    def get_serializer_class(self):
        if self.action == 'report':
            return serializers.ReportSerializer
        elif self.action == 'skip_image':
            return serializers.ImagesViewedSerializer
        elif self.action != 'like_image':
            return serializers.ImageCreateSerializer
        else:
            return serializers.LikeImageSerializer

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [permissions.IsAuthenticated, CanPostOrBan]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        account = get_object_or_404(Account, user=self.request.user)
        serializer.save(account=account)

    def get_queryset(self):
        return models.Image.objects.alias(Count('reports')).filter(reports__count__lte=10).exclude(
            account__user=self.request.user).exclude(images_viewed_by_user__user__user=self.request.user).order_by('?')

    @action(detail=False)
    def top_5(self, request):
        return Response(serializers.ImageCreateSerializer(
            models.Image.objects.alias(Count('reports')).filter(reports__count__lte=10).alias(Count('likes')).order_by(
                '-likes__count')[:5], many=True).data)

    @action(methods=['post'], detail=True)
    def like_image(self, request, pk=None):
        image = get_object_or_404(models.Image, pk=pk)
        account = get_object_or_404(Account, user=self.request.user)
        obj = models.Like.objects.create(image=image, user=account)
        serializer = self.get_serializer_class()(obj)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def skip_image(self, request, pk=None):
        account = get_object_or_404(Account, user=self.request.user)
        obj, _ = models.ImagesViewed.objects.get_or_create(user=account)
        image = get_object_or_404(models.Image, pk=pk)
        obj.images.add(image)
        serializer = self.get_serializer_class()(obj)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def report(self, request, pk=None):
        account = get_object_or_404(Account, user=self.request.user)
        image = get_object_or_404(models.Image, pk=pk)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(user=account, image=image)
        return Response(serializer.data)
