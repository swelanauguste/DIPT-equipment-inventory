import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Ticket
from .tasks import (
    ticket_comment_created_email,
    ticket_created_email,
    ticket_updated_email,
)


@receiver(post_save, sender=Comment)
def ticket_comment_created_email_signal(sender, instance, created, **kwargs):
    if created:
        ticket_comment_created_email_thread = threading.Thread(
            target=ticket_comment_created_email, args=(instance,)
        )
        ticket_comment_created_email_thread.start()
    # else:
    #     ticket_update_email_thread = threading.Thread(
    #         target=ticket_updated_email, args=(instance,)
    #     )
    #     ticket_update_email_thread.start()


@receiver(post_save, sender=Ticket)
def ticket_created_email_signal(sender, instance, created, **kwargs):
    if created:
        ticket_created_email_thread = threading.Thread(
            target=ticket_created_email, args=(instance,)
        )
        ticket_created_email_thread.start()
    else:
        ticket_update_email_thread = threading.Thread(
            target=ticket_updated_email, args=(instance,)
        )
        ticket_update_email_thread.start()
