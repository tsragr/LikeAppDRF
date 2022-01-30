from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response
from knox.models import AuthToken
from account.serializers import RegisterSerializer, UserSerializer, AccountSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from account.models import Account
from account.tasks import send_welcome_email


class RegisterAPI(generics.GenericAPIView):
    """
    View to register user
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    """
    Login View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        send_welcome_email.delay(request.user.email)
        return super().post(request, format=None)


class AccountCreateUpdateViewSet(viewsets.GenericViewSet,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 ):
    """
    View to get or edit user's account
    """

    serializer_class = AccountSerializer
    queryset = Account.objects.all()

