# reports/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ReportRequest
from .tasks import generate_user_report

@login_required
def generate_report(request):
    if request.method == 'POST':
        report = ReportRequest.objects.create(user=request.user)
        generate_user_report.delay(report.id)
        return render(request, 'reports/success.html', {'report': report})
    return render(request, 'reports/generate_report.html')
