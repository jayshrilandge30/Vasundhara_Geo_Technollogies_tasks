from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
# from .tasks import generate_report_task
from .tasks import generate_pdf_report_task



def generate_report_view(request):
    user_email = "testuser@example.com"  # hardcoded email for testing
    generate_pdf_report_task.delay(user_email)
    return JsonResponse({"message": "Report generation started. Check the Celery worker for the download link."})

