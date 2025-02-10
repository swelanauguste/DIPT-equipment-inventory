from django.shortcuts import render
from tickets.models import Ticket
from users.models import Department, User


def get_department_stats(request):
    tickets = Ticket.objects.all()

    context = {
    }
    return render(request, "reports/reports.html", context)
