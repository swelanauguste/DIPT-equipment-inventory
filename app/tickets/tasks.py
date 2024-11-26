from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


def ticket_created_email(instance):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"Ticket {instance.ticket_id.upper()}"
    ticket_url = reverse("ticket-detail", kwargs={"slug": instance.slug})
    full_url = f"https://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_created_email.html",
        {"ticket": instance, "full_url": full_url},
    )
    plain_message = strip_tags(html_message)

    if instance.created_by:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                instance.created_by.email,
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )
    else:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )


def ticket_updated_email(instance):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"Ticket {instance.ticket_id.upper()}"
    ticket_url = reverse("ticket-detail", kwargs={"slug": instance.slug})
    full_url = f"https://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_update_email.html",
        {"ticket": instance, "full_url": full_url},
    )
    plain_message = strip_tags(html_message)

    if instance.created_by:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                instance.created_by.email,
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )
    else:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )


def ticket_comment_created_email(instance):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"Ticket {instance.ticket.ticket_id.upper()}"
    ticket_url = reverse("ticket-detail", kwargs={"slug": instance.ticket.slug})
    full_url = f"https://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_comment_email.html",
        {"comment": instance, "full_url": full_url},
    )
    plain_message = strip_tags(html_message)

    if instance.created_by:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                instance.created_by.email,
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )
    else:
        send_mail(
            subject,  # subject of email
            plain_message,  # body of email
            settings.DEFAULT_FROM_EMAIL,  # from email
            [
                settings.DEFAULT_FROM_EMAIL,
            ],  # to emails
            html_message=html_message,
        )
