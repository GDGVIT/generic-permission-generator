from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import UserCreationSerializer


class UserCreation(generics.CreateAPIView):
    serializer_class = UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            get_user_model().objects.create_user(**dict(serializer.validated_data))
        except Exception as e:
            print(e)
            Response.status_code = 406
            return Response({"err": "Unable to add user"})
        return Response({"msg": "User successfully added"})


