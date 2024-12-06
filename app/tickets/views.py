from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.models import User

from . import forms, models


class TicketListView(LoginRequiredMixin, ListView):
    model = models.Ticket
    paginate_by = 20
    template_name = "tickets/tech/ticket_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_deleted=False)

        # Retrieve filter parameters
        is_closed = self.request.GET.get("is_closed", "")
        ticket_status = self.request.GET.get("ticket_status", "")
        ticket_category = self.request.GET.get("ticket_category", "")
        query = self.request.GET.get("q", "")
        assigned_to = self.request.GET.get("assigned_to", "")

        # Apply filters
        if ticket_category:
            category_ids = ticket_category.split(",")
            queryset = queryset.filter(ticket_category__id__in=category_ids)

        if is_closed:
            queryset = queryset.filter(is_closed=(is_closed.lower() == "true"))
        if ticket_status:
            queryset = queryset.filter(ticket_status_id=ticket_status)

        if query:
            queryset = queryset.filter(
                Q(summary__icontains=query) | Q(description__icontains=query)
            )
        if assigned_to:
            if assigned_to == "unassigned":
                queryset = queryset.filter(assigned_to__isnull=True)
            else:
                queryset = queryset.filter(assigned_to_id=assigned_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options for dropdowns
        context["ticket_count"] = self.get_queryset().filter(is_deleted=False).count()
        context["statuses"] = models.TicketStatus.objects.all()
        context["categories"] = models.TicketCategory.objects.all()
        context["users"] = User.objects.filter(role__in=["technician", "manager"])

        # Get selected categories as a list
        selected_categories = self.request.GET.getlist("ticket_category")
        context["selected_categories"] = [
            int(category) for category in selected_categories
        ]

        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context


class UserTicketListView(LoginRequiredMixin, ListView):
    model = models.Ticket
    paginate_by = 20
    template_name = "tickets/users/ticket_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = (
            super()
            .get_queryset()
            .filter(Q(is_deleted=False) & (Q(created_by=user) | Q(user=user)))
        )

        # Retrieve filter parameters
        is_closed = self.request.GET.get("is_closed", "")
        ticket_status = self.request.GET.get("ticket_status", "")
        ticket_category = self.request.GET.get("ticket_category", "")
        query = self.request.GET.get("q", "")
        assigned_to = self.request.GET.get("assigned_to", "")

        # Apply filters
        if is_closed:
            queryset = queryset.filter(is_closed=(is_closed.lower() == "true"))
        if ticket_status:
            queryset = queryset.filter(ticket_status_id=ticket_status)
        if ticket_category:
            queryset = queryset.filter(ticket_category_id=ticket_category)
        if query:
            queryset = queryset.filter(
                Q(summary__icontains=query) | Q(description__icontains=query)
            )
        if assigned_to:
            if assigned_to == "unassigned":
                queryset = queryset.filter(assigned_to__isnull=True)
            else:
                queryset = queryset.filter(assigned_to_id=assigned_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options for dropdowns
        context["ticket_count"] = (
            models.Ticket.objects.filter(is_deleted=False)
            .filter(created_by=self.request.user)
            .count()
        )
        context["statuses"] = models.TicketStatus.objects.all()
        context["categories"] = models.TicketCategory.objects.all()
        context["users"] = User.objects.filter(role__in=["technician", "manager"])

        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = models.Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = forms.CommentCreateForm()
        return context


class TicketUserCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketUserForm
    template_name = "tickets/users/ticket_user_create.html"

    def form_valid(self, form):
        # Add the logged-in user to the ManyToMany field
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        form.instance.user.add(self.request.user)
        return response


class TicketUserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    form_class = forms.TicketUserForm
    template_name = "tickets/users/ticket_user_update.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TicketTechnicianCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketTechCreateForm
    template_name = "tickets/tech/ticket_tech_create.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TicketTechUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    form_class = forms.TicketTechUpdateForm
    template_name = "tickets/tech/ticket_tech_update.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


def ticket_delete_view(request, slug):
    ticket = get_object_or_404(models.Ticket, slug=slug)
    ticket.is_deleted = True
    ticket.deleted_at = timezone.now()
    ticket.deleted_by = request.user
    ticket.save()

    return redirect("ticket-list")

    # If the form is not valid or the request method is not POST
    return render(
        request, "tickets/ticket_detail.html", {"ticket": ticket, "comment_form": form}
    )


def ticket_close_view(request, slug):
    ticket = get_object_or_404(models.Ticket, slug=slug)
    closed_status = get_object_or_404(models.TicketStatus, name__icontains="closed")
    ticket.ticket_status = closed_status
    ticket.is_closed = True
    ticket.closed_at = timezone.now()
    ticket.closed_by = request.user
    ticket.save()

    return redirect("ticket-detail", slug=slug)

    # If the form is not valid or the request method is not POST
    return render(
        request, "tickets/ticket_detail.html", {"ticket": ticket, "comment_form": form}
    )


def add_comment_view(request, slug):
    ticket = get_object_or_404(models.Ticket, slug=slug)

    if request.method == "POST":
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            if request.user.is_authenticated:
                comment.created_by = request.user
                comment.updated_by = request.user
            comment.save()
            return redirect("ticket-detail", slug=slug)

    # If the form is not valid or the request method is not POST
    return render(
        request, "tickets/ticket_detail.html", {"ticket": ticket, "comment_form": form}
    )
