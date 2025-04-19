from accounts.permissions import IsEmployerOrAdmin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import JobCreateSerializer


class JobCreateView(APIView):
    permission_classes = (IsEmployerOrAdmin,)

    def post(self, request):
        user = request.user
        serializer = JobCreateSerializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.validated_data)
        return Response(
            {
                "message": "Job created successfully!",
                "data": {**serializer.data, "owner": user.email},
            },
            status=status.HTTP_201_CREATED,
        )
