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



import os
import json
from datetime import datetime
from django.conf import settings
from celery import shared_task
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@shared_task
def generate_pdf_report_task(user_email):
    # Load JSON data
    json_path = os.path.join(settings.BASE_DIR, 'data', 'users.json')
    with open(json_path, 'r') as f:
        users = json.load(f)

    # File name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"user_report_{timestamp}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)

    # Create PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    y = height - 50
    c.drawString(50, y, f"User Report - Generated for {user_email}")
    y -= 30

    for user in users:
        c.drawString(50, y, f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
        y -= 20
        profile = user['profile']
        c.drawString(70, y, f"Profile - Age: {profile['age']}, Location: {profile['location']}, Designation: {profile['designation']}")
        y -= 20
        activities = ", ".join(user['activities'])
        c.drawString(70, y, f"Activities: {activities}")
        y -= 30

        # Add page if space runs out
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50

    c.save()

    # Instead of email, just print the download link
    download_link = os.path.join(settings.MEDIA_URL, 'reports', file_name)
    print(f"Report generated for {user_email}. Download link: {download_link}")

    return download_link
