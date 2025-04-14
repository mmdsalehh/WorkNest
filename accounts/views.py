from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginViewSerializer, RegisterViewSerializer


class RegisterView(APIView):
    serializer_class = RegisterViewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, token = serializer.create(serializer.validated_data)
        return Response(
            {
                "message": "User registered successfully!",
                "user": serializer.data,
                "token": token.key,
            }
        )


class LoginView(APIView):
    serializer_class = LoginViewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.login(serializer.validated_data)
        return Response(
            {
                "message": "User logged in successfully!",
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
                "token": token.key,
            }
        )
