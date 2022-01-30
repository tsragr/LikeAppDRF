from django.contrib import admin
from likeapp import models


@admin.register(models.Image)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'account')


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'text')


admin.site.register(models.ImagesViewed)
