from rest_framework.routers import DefaultRouter
from likeapp import views

router = DefaultRouter()

router.register('img', views.ImageRetrieveCreateViewSet, basename='image')

urlpatterns = router.urls
