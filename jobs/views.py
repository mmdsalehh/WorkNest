from accounts.permissions import IsEmployerOrAdmin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Job
from .pagination import JobsListPagination
from .serializers import JobCreateSerializer, JobListSerializer


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


class JobListView(APIView):
    SORT_MAP = {
        "latest": "-created_at",
        "earliest": "created_at",
        "salary_highest": "-salary",
        "salary_lowest": "salary",
    }

    def get(self, request):
        sort_key = request.query_params.get("sort", "latest")
        sort_by = self.SORT_MAP.get(sort_key, "-created_at")

        jobs_qs = Job.objects.all().order_by(sort_by)
        # TODO: Add filtering logic here

        paginator = JobsListPagination()
        paginated_jobs = paginator.paginate_queryset(jobs_qs, request)
        serializer = JobListSerializer(paginated_jobs, many=True)

        pagination_data = {
            "count": paginator.page.paginator.count,
            "has_next": paginator.page.has_next(),
            "has_previous": paginator.page.has_previous(),
            "page": paginator.page.number,
        }

        return Response(
            {
                "message": "Jobs retrieved successfully!",
                "data": serializer.data,
                "sort": sort_key,
                "pagination": pagination_data,
            },
            status=status.HTTP_200_OK,
        )
