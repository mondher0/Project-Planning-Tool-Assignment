from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView
from .export_pdf_view import ProjectExportPDFView
from .send_email_view import SendEmailView
from .generate_summarize_view import GenerateSummarizeView

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
    path(
        "generate_summarize",
        GenerateSummarizeView.as_view(),
        name="generate-summarize",
    ),
]
