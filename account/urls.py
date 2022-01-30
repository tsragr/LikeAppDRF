from django.urls import path
from account import views
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

router = DefaultRouter()

router.register('my_account', views.AccountCreateUpdateViewSet, basename='my account')

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]

urlpatterns += router.urls
