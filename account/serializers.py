from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Account
from likeapp.serializers import ImageCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated users
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class AccountSerializer(serializers.ModelSerializer):
    """
    User's account serializer
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    images = ImageCreateSerializer(read_only=True, many=True)

    class Meta:
        model = Account
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration serializer
    """
    password_confirm = serializers.CharField(write_only=True)
    account = AccountSerializer(write_only=True)

    class Meta:
        model = User
        fields = ('account', 'username', 'email', 'password', 'password_confirm')

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        if validated_data['password'] == validated_data['password_confirm']:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email']
            )
            Account.objects.create(user=user, **account_data)
        return user
