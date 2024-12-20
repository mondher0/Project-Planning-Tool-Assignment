from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project
from .utils import send_project_email


class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        recipient_email = request.data.get("recipient_email")
        include_pdf = request.data.get("include_pdf", False)

        if not recipient_email:
            return Response(
                {"error": "Recipient email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            send_project_email(project, recipient_email, include_pdf)
            return Response(
                {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
