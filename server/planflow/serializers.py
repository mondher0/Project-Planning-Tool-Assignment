from rest_framework import serializers
from .models import Project, ProjectImage
from django.core.exceptions import ValidationError


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["image"]

    def validate_image(self, value):
        # Check the file type (MIME type)
        if not value.name.endswith(("jpg", "jpeg", "png", "gif")):
            raise serializers.ValidationError(
                "Invalid image format. Only JPG, JPEG, PNG, and GIF are allowed."
            )

        # Check the file size (e.g., max size 5 MB)
        if value.size > 5 * 1024 * 1024:  # 5 MB
            raise serializers.ValidationError("Image size should not exceed 5 MB.")

        return value


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "priority",
            "category",
            "status",
            "images",
            "uploaded_images",
        ]

    def create(self, validated_data):
        print(validated_data)
        uploaded_images = validated_data.pop("uploaded_images", [])
        print(uploaded_images)
        project = Project.objects.create(**validated_data)

        for image in uploaded_images:
            # validate image using the ProjectImageSerializer
            project_image_serializer = ProjectImageSerializer(data={"image": image})
            if project_image_serializer.is_valid():
                ProjectImage.objects.create(project=project, image=image)
            else:
                # If the image validation fails, raise an error
                raise serializers.ValidationError(project_image_serializer.errors)

        return project

    def update(self, instance, validated_data):
        print(validated_data)
        uploaded_images = validated_data.pop("uploaded_images", [])
        instance = super().update(instance, validated_data)

        # Remove old images
        instance.images.all().delete()

        # Create new images
        for image in uploaded_images:
            # validate image using the ProjectImageSerializer
            project_image_serializer = ProjectImageSerializer(data={"image": image})
            if project_image_serializer.is_valid():
                ProjectImage.objects.create(project=instance, image=image)
            else:
                # If the image validation fails, raise an error
                raise serializers.ValidationError(project_image_serializer.errors)

        return instance
