from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated


# Pagination class
class ProjectPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum items per page


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For file uploads (images)

    def get(self, request):
        projects = Project.objects.filter(
            user=request.user
        )  # Only fetch projects for the authenticated user
        paginator = ProjectPagination()
        result_page = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign the user to the project
            return Response(
                {
                    "message": "Project created successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For file uploads (images)

    def get_object(self, project_id):
        try:
            return Project.objects.get(
                id=project_id, user=self.request.user
            )  # Ensure user is the project owner
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(
            project,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Updates the project
            return Response(
                {
                    "message": "Project updated successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )

        project.delete()
        return Response(
            {"message": "Project deleted successfully!"}, status=status.HTTP_200_OK
        )
