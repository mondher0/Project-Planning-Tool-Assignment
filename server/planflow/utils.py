from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from io import BytesIO
from .models import ProjectImage


def generate_project_pdf(project):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    margin = 50  # Left and right margins
    y_position = height - 50  # Start just below the top margin
    x_position = margin  # Start at the left margin
    image_width, image_height = 150, 100  # Size of each image
    spacing = 10  # Space between images

    def check_space_for_image():
        """Check if there's enough space for the next image, and handle wrapping or new pages."""
        nonlocal x_position, y_position
        if (
            x_position + image_width > width - margin
        ):  # Wrap to next line if out of horizontal space
            x_position = margin  # Reset to left margin
            y_position -= image_height + spacing  # Move down for the next row
        if y_position - image_height < margin:  # Check if there's enough vertical space
            p.showPage()  # Add a new page
            p.setFont("Helvetica", 12)  # Reset font for the new page
            x_position = margin  # Reset horizontal position
            y_position = height - 50  # Reset vertical position for the new page

    # Add title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(margin, y_position, f"Project Title: {project.title}")
    y_position -= 30

    # Add description
    p.setFont("Helvetica", 12)
    description = project.description
    p.drawString(margin, y_position, f"Description: {description}")
    y_position -= 20

    # Add dates
    p.drawString(margin, y_position, f"Start Date: {project.start_date}")
    y_position -= 20
    p.drawString(margin, y_position, f"End Date: {project.end_date}")
    y_position -= 20

    # Add priority, category, status
    p.drawString(margin, y_position, f"Priority: {project.priority}")
    y_position -= 20
    p.drawString(margin, y_position, f"Category: {project.category}")
    y_position -= 20
    p.drawString(margin, y_position, f"Status: {project.status}")
    y_position -= 40

    # Add images (if any)
    images = ProjectImage.objects.filter(project=project)
    if images:
        p.drawString(margin, y_position, "Images: ")
        y_position -= 20
    for image in images:
        image_path = default_storage.path(image.image.name)
        check_space_for_image()  # Ensure there's space before adding the next image
        p.drawImage(
            image_path,
            x_position,
            y_position - image_height,
            width=image_width,
            height=image_height,
        )
        x_position += (
            image_width + spacing
        )  # Move to the next position for the next image

    # Finalize and save the PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def send_project_email(project, recipient_email, include_pdf=False):
    subject = f"Project Details: {project.title}"

    # Collect images and prepare them for attachment
    images = ProjectImage.objects.filter(project=project)
    attachments = []  # For attached images

    for image in images:
        image_path = default_storage.path(image.image.name)
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
            mime_image = MIMEImage(img_data)
            # Set the filename for the image attachment
            mime_image.add_header(
                "Content-Disposition", "attachment", filename=image.image.name
            )
            attachments.append(mime_image)

    # Render the email content (without images embedded)
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

    # Create the email
    email = EmailMessage(subject, message, None, [recipient_email])
    email.content_subtype = "html"  # Set content type to HTML

    # Attach images as file attachments
    for attachment in attachments:
        email.attach(attachment)

    # Attach the PDF (if requested)
    if include_pdf:
        pdf_buffer = generate_project_pdf(project)
        email.attach(f"{project.title}.pdf", pdf_buffer.getvalue(), "application/pdf")

    # Send the email
    email.send()
