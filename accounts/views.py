from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        return Response('hello')
