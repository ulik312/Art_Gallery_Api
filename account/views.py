from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from account .tasks import send_activation_codee
from rest_framework.views import APIView
from .serializers import *

#TODO: register view
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully signed up", status=status.HTTP_201_CREATED)


#TODO: activate view
class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account successfully activated!", status=status.HTTP_200_OK)


#TODO: login view
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

#TODO: logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Succesfully logged out', status=status.HTTP_200_OK)



class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_codee.delay(str(user.email), str(user.activation_code))
        return Response('Вам отправлено смс', status=status.HTTP_200_OK)

class ForgotPasswordComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=status.HTTP_200_OK)
