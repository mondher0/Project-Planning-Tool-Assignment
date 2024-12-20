from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView
from .export_pdf_view import ProjectExportPDFView
from .send_email_view import SendEmailView

urlpatterns = [
    path(
        "", ProjectListCreateView.as_view(), name="project-list-create"
    ),  # List and Create
    path(
        "<int:project_id>", ProjectDetailView.as_view(), name="project-detail"
    ),  # Retrieve, Update, Delete
    path(
        "<int:project_id>/export_pdf",
        ProjectExportPDFView.as_view(),
        name="project-export-pdf",
    ),
    path(
        "<int:project_id>/send_email",
        SendEmailView.as_view(),
        name="send-email",
    ),
]
