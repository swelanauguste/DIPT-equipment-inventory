from django.core.management.base import BaseCommand
from tickets.models import Comment, Ticket
from users.models import User

# swelan = "swelan.auguste@govt.lc" = 18
# desiree = "desiree.jnbaptiste@govt.lc" pk=20
# roxanne = "roxanne.francois@govt.lc" pk=2
# perpetua = "perpetua.dieudonna@govt.lc" pk=3




class Command(BaseCommand):

    def handle(self, *args, **options):
        # user = User.objects.get(email=swelan)
        # print(user)
        # user.set_password('password3')
        # user.username = 'swelanauguste'
        # user.save()
        users = User.objects.all()[:5]
        # print(users.count())
        for user in users:
            print(user.email)
        #     user.set_password("Password2024")
        #     user.save()
    # def handle(self, *args, **options):
    #     swelan_comments = Comment.objects.filter(created_by__email=perpetua)
    #     desiree_comments = Comment.objects.filter(created_by__email=roxanne)
        
    #     for comment in swelan_comments:
    #         comment.created_by = User.objects.get(email=swelan)
    #         comment.save()

    #     for comment in desiree_comments:
    #         comment.created_by = User.objects.get(email=desiree)
    #         comment.save()


#         # tickets = Ticket.objects.filter(assigned_to__email="perpetua.dieudonna@govt.lc")
#         # print(tickets.count())
#         # for ticket in tickets:
#         #     ticket.assigned_to = User.objects.get(email="swelan.auguste@govt.lc")
#         #     print(ticket)
#         #     ticket.save()

#         # tickets = Ticket.objects.filter(updated_by__email="roxanne.francois@govt.lc")
#         # print(tickets.count())
#         # for ticket in tickets:
#         #     ticket.updated_by = User.objects.get(email="desiree.jnbaptiste@govt.lc")
#         #     print(ticket)
#         #     ticket.save()
