# from celery import shared_task
# import os, json
# from django.conf import settings



#     # Later: generate PDF, save to media/reports/, send email
# import os
# import json
# from datetime import datetime
# from django.conf import settings
# from celery import shared_task
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

# @shared_task
# def generate_pdf_report_task(user_email):
#     # Load JSON data
#     json_path = os.path.join(settings.BASE_DIR, 'data', 'users.json')
#     with open(json_path, 'r') as f:
#         users = json.load(f)

#     # File name with timestamp
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     file_name = f"user_report_{timestamp}.pdf"
#     file_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)

#     # Create PDF
#     c = canvas.Canvas(file_path, pagesize=letter)
#     width, height = letter
#     c.setFont("Helvetica", 12)

#     y = height - 50
#     c.drawString(50, y, f"User Report - Generated for {user_email}")
#     y -= 30

#     for user in users:
#         c.drawString(50, y, f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
#         y -= 20
#         profile = user['profile']
#         c.drawString(70, y, f"Profile - Age: {profile['age']}, Location: {profile['location']}, Designation: {profile['designation']}")
#         y -= 20
#         activities = ", ".join(user['activities'])
#         c.drawString(70, y, f"Activities: {activities}")
#         y -= 30

#         # Add page if space runs out
#         if y < 50:
#             c.showPage()
#             c.setFont("Helvetica", 12)
#             y = height - 50

#     c.save()

#     # Return file path
#     return os.path.join(settings.MEDIA_URL, 'reports', file_name)


# reports/tasks.py
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from .models import ReportRequest
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task(bind=True)
def generate_user_report(self, report_id):
    try:
        report = ReportRequest.objects.get(id=report_id)
        report.status = 'IN_PROGRESS'
        report.progress = 10
        report.save()

        # Generate PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, "User Report")
        p.setFont("Helvetica", 10)
        p.drawString(50, height - 70, f"Requested by: {report.user.username}")
        p.drawString(50, height - 85, f"Generated on: {timezone.now()}")

        y = height - 120
        users = User.objects.all().order_by('id')

        for u in users:
            if y < 100:
                p.showPage()
                y = height - 50
            p.drawString(50, y, u.username)
            p.drawString(200, y, u.email or "No Email")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)

        # Ensure folder exists
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'reports'), exist_ok=True)

        # Save PDF in FileField
        file_name = f"user_report_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
        report.file.save(file_name, ContentFile(buffer.read()), save=False)
        report.status = 'COMPLETED'
        report.progress = 100
        report.completed_at = timezone.now()
        report.save()

        # Email with link
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        download_link = f"{site_url}{settings.MEDIA_URL}{report.file.name}"

        send_mail(
            subject='Your report is ready',
            message=f"Your report is ready!\n\nDownload: {download_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[report.user.email],
            fail_silently=False,
        )
        return "Report generated successfully."

    except Exception as e:
        report.status = 'FAILED'
        report.save()
        raise e

