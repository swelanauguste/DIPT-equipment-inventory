from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.models import User

from . import forms, models


class TicketListView(LoginRequiredMixin, ListView):
    model = models.Ticket
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve filter parameters
        is_closed = self.request.GET.get("is_closed", "")
        ticket_status = self.request.GET.get("ticket_status", "")
        ticket_category = self.request.GET.get("ticket_category", "")
        summary = self.request.GET.get("summary", "")
        description = self.request.GET.get("description", "")
        assigned_to = self.request.GET.get("assigned_to", "")

        # Apply filters
        if is_closed:
            queryset = queryset.filter(is_closed=(is_closed.lower() == "true"))
        if ticket_status:
            queryset = queryset.filter(ticket_status_id=ticket_status)
        if ticket_category:
            queryset = queryset.filter(ticket_category_id=ticket_category)
        if summary:
            queryset = queryset.filter(summary__icontains=summary)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if assigned_to:
            if assigned_to == "unassigned":
                queryset = queryset.filter(assigned_to__isnull=True)
            else:
                queryset = queryset.filter(assigned_to_id=assigned_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options for dropdowns
        context["statuses"] = models.TicketStatus.objects.all()
        context["categories"] = models.TicketCategory.objects.all()
        context["users"] = User.objects.filter(role__in=["technician", "manager"])
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = models.Ticket


class TicketUserCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketUserForm
    template_name = "tickets/users/ticket_user_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TicketUserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    form_class = forms.TicketTechUpdateForm
    template_name = "tickets/tech/ticket_user_update.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TicketTechnicianCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketTechCreateForm
    template_name = "tickets/tech/ticket_tech_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketTechUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    form_class = forms.TicketTechUpdateForm
    template_name = "tickets/tech/ticket_tech_update.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
