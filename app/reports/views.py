import csv
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from tickets.models import Ticket, TicketCategory, TicketStatus


def ticket_report_view(request):
    tickets_by_status = {
        status.name: Ticket.objects.filter(ticket_status=status)
        for status in TicketStatus.objects.all()
    }

    # Check if the request asks for a CSV export
    if "export" in request.GET and request.GET["export"] == "csv":
        return export_tickets_to_csv(tickets_by_status)

    context = {
        "tickets_by_status": tickets_by_status,
    }

    return render(request, "reports/reports.html", context)


def export_tickets_to_csv(tickets_by_status):
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="ticket_report{current_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["Ticket Status", "Ticket ID", "Summary", "Assigned to", "Created At"]
    )  # CSV Header

    for status, tickets in tickets_by_status.items():
        for ticket in tickets:
            writer.writerow(
                [
                    status,
                    ticket.ticket_id.upper(),
                    ticket.summary,
                    ticket.assigned_to,
                    ticket.created_at,
                ]
            )

    return response
