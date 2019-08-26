import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, format='json'):
        username = json.loads(request.body).get("username")
        password = json.loads(request.body).get("password")
        errors = {}

        if password is None:
            errors["password"] = "this field is required"
        if username is None:
            errors["username"] = "this field is required"
        if "password" in errors or "username" in errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username)
        if len(user) == 0:
            return Response({
                "username": "username not found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                "password": "wrong password"
            }, status=status.HTTP_401_UNAUTHORIZED)

        token = Token.objects.filter(user=user)
        if len(token) == 0:
            token = Token(user=user)
            token.save()
        else:
            token = token[0]

        return Response({
            "id": user.id,
            "username": username,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_202_ACCEPTED)
