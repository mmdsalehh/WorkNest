from rest_framework import serializers

from .models import Job


class JobCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Job.objects.create(
            owner=self.context["user"],
            **validated_data,
        )

    class Meta:
        model = Job
        fields = (
            "title",
            "description",
            "type",
            "location",
            "company",
            "salary",
        )

        extra_kwargs = {"salary": {"required": True}}


class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "description",
            "type",
            "location",
            "company",
            "salary",
            "is_active",
        )
        read_only_fields = fields
