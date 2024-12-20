from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from io import BytesIO
from .models import ProjectImage


def generate_project_pdf(project):
    """Generates a PDF document for the given project."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50
    y_position = height - 50
    x_position = margin
    image_width, image_height = 150, 100
    spacing = 10

    def add_image(image_path):
        """Add an image to the PDF at the current position."""
        nonlocal x_position, y_position
        if x_position + image_width > width - margin:  # Wrap to next line
            x_position = margin
            y_position -= image_height + spacing
        if (
            y_position - image_height < margin
        ):  # Add a new page if space is insufficient
            p.showPage()
            p.setFont("Helvetica", 12)
            x_position = margin
            y_position = height - 50
        p.drawImage(
            image_path,
            x_position,
            y_position - image_height,
            width=image_width,
            height=image_height,
        )
        x_position += image_width + spacing

    # Title, description, and project details
    p.setFont("Helvetica-Bold", 18)
    p.drawString(margin, y_position, f"Project Title: {project.title}")
    y_position -= 30
    p.setFont("Helvetica", 12)
    p.drawString(margin, y_position, f"Description: {project.description}")
    y_position -= 20
    p.drawString(margin, y_position, f"Start Date: {project.start_date}")
    y_position -= 20
    p.drawString(margin, y_position, f"End Date: {project.end_date}")
    y_position -= 20
    p.drawString(margin, y_position, f"Priority: {project.priority}")
    y_position -= 20
    p.drawString(margin, y_position, f"Category: {project.category}")
    y_position -= 20
    p.drawString(margin, y_position, f"Status: {project.status}")
    y_position -= 40

    # Add images
    images = ProjectImage.objects.filter(project=project)
    if images:
        p.drawString(margin, y_position, "Images: ")
        y_position -= 20
    for image in images:
        image_path = default_storage.path(image.image.name)
        add_image(image_path)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def prepare_project_email(project, recipient_email):
    """Prepares the email with project details and attachments."""
    subject = f"Project Details: {project.title}"
    message = render_to_string(
        "emails/project_description.html",
        {
            "title": project.title,
            "description": project.description,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "priority": project.priority,
            "category": project.category,
            "status": project.status,
        },
    )

    email = EmailMessage(subject, message, None, [recipient_email])
    email.content_subtype = "html"

    return email


def attach_images_to_email(email, project):
    """Attaches project images to the email."""
    images = ProjectImage.objects.filter(project=project)
    for image in images:
        image_path = default_storage.path(image.image.name)
        email.attach_file(image_path)  # Attach image file

    return email


def attach_pdf_to_email(email, project, include_pdf=False):
    """Attaches a PDF file of the project details to the email."""
    if include_pdf:
        pdf_buffer = generate_project_pdf(project)
        email.attach(f"{project.title}.pdf", pdf_buffer.getvalue(), "application/pdf")

    return email


def send_project_email(project, recipient_email, include_pdf=False):
    """Generates the email and sends it with the project details, images, and PDF."""
    email = prepare_project_email(project, recipient_email)
    email = attach_images_to_email(email, project)
    email = attach_pdf_to_email(email, project, include_pdf)

    email.send()
