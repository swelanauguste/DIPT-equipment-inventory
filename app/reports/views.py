import csv
from datetime import datetime

from computers.models import Computer, Status
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from tickets.models import Ticket, TicketCategory, TicketStatus
from users.models import User


def ticket_report_view(request):

    users_with_more_than_2_tickets = (
        User.objects.annotate(ticket_count=Count("tickets"))
        .filter(ticket_count__gte=2)
        .order_by("-ticket_count")
    )

    tickets_by_status = {
        status.name: Ticket.objects.filter(ticket_status=status)
        for status in TicketStatus.objects.all()
    }

    # Check if the request asks for a CSV export
    if (
        "export_tickets" in request.GET
        and request.GET["export_tickets"] == "tickets_csv"
    ):
        return export_tickets_to_csv(tickets_by_status)

    computers_by_status = {
        status.name: Computer.objects.filter(status=status)
        for status in Status.objects.all()
    }
    # Check if the request asks for a CSV export
    if (
        "export_computers" in request.GET
        and request.GET["export_computers"] == "computers_csv"
    ):
        return export_computers_to_csv(computers_by_status)

    context = {
        "tickets_by_status": tickets_by_status,
        "computers_by_status": computers_by_status,
        "users_with_more_than_2_tickets": users_with_more_than_2_tickets,
    }

    return render(request, "reports/reports.html", context)


def export_tickets_to_csv(tickets_by_status):
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="ticket_report{current_date}.csv"'
    )

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


def export_computers_to_csv(computers_by_status):
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="computer_report{current_date}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "status",
            "from_project",
            "serial_number",
            "warranty_info",
            "computer_name",
            "model",
            "monitor",
            "os",
            "location",
            "department",
            "user",
            "date_received",
            "date_installed",
            "notes",
        ]
    )  # CSV Header

    for status, computers in computers_by_status.items():
        for computer in computers:
            writer.writerow(
                [
                    status,
                    computer.from_project,
                    computer.serial_number.upper(),
                    computer.warranty_info,
                    computer.computer_name,
                    computer.model.name.upper(),
                    computer.monitor.first(),
                    computer.os,
                    computer.location,
                    computer.department,
                    computer.user.first(),
                    computer.date_received,
                    computer.date_installed,
                    computer.notes.upper(),
                ]
            )

    return response
