from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Project
from rest_framework.permissions import IsAuthenticated
from .utils import (
    generate_project_pdf,
)


class ProjectExportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id):
        try:
            return Project.objects.get(id=project_id, user=self.request.user)
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        project = self.get_object(project_id)
        if project is None:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Generate PDF
        pdf_buffer = generate_project_pdf(project)

        # Create response with PDF file
        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="project_{project_id}.pdf"'
        )
        return response
