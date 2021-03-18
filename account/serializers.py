from django.contrib.auth import authenticate
from rest_framework import serializers

from account.tasks import send_activation_code

from account.models import MyUser




#TODO: register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        """This function is called when self.save() method is called"""
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code.delay(str(user.email), str(user.activation_code))
        return user



#TODO: login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email,
                                password=password)

            if not user:
                message = 'Unable to login with provided credentials'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Must include "email" and "password"'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(max_length=255, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email не найден')
        return email

    def validate_activation_code(self, code):
        if not MyUser.objects.filter(activation_code=code, is_active=False).exists():
            print('sdfd')
            raise serializers.ValidationError('Не верный код активации')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email  = data.get('email')
        code = data.get('activation_code')
        password = data.get('password')
        try:

            user = MyUser.objects.get(email=email, activation_code=code, is_active=False)

        except MyUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
