from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.user_permission import UserAccessMixin

from . import forms, models


class MicrosoftOfficeListView(UserAccessMixin, ListView):
    model = models.MicrosoftOffice
    paginate_by = 20

    def get_queryset(self):
        queryset = models.MicrosoftOffice.objects.all()
        no_assignment = self.request.GET.get(
            "no_assignment"
        )  # Check for a filter param
        if no_assignment == "1":
            queryset = queryset.filter(assignments__isnull=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_count"] = self.get_queryset().count()
        return context


class MicrosoftOfficeDetailView(UserAccessMixin, DetailView):
    model = models.MicrosoftOffice


class MicrosoftOfficeCreateView(UserAccessMixin, CreateView):
    model = models.MicrosoftOffice
    form_class = forms.MicrosoftOfficeForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MicrosoftOfficeUpdateView(UserAccessMixin, UpdateView):
    model = models.MicrosoftOffice
    form_class = forms.MicrosoftOfficeForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MicrosoftOfficeAssignView(UserAccessMixin, CreateView):
    model = models.MicrosoftOfficeAssignment
    form_class = forms.MicrosoftOfficeAssignmentForm

    def get_initial(self):
        """Set the initial Microsoft Office key if accessed via a specific key's page."""
        microsoft_office_id = self.kwargs.get("pk")
        microsoft_office = get_object_or_404(
            models.MicrosoftOffice, pk=microsoft_office_id
        )
        return {"microsoft_office": microsoft_office}

    def form_valid(self, form):
        """Ensure the Microsoft Office key is set and the user details are added."""
        microsoft_office_id = self.kwargs.get("pk")
        microsoft_office = get_object_or_404(
            models.MicrosoftOffice, pk=microsoft_office_id
        )
        form.instance.microsoft_office = microsoft_office
        form.instance.assigned_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     """Redirect back to the detail page for the assigned Office key."""
    #     return reverse(
    #         "microsoft-office-detail", kwargs={"pk": self.object.microsoft_office.pk}
    #     )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        microsoft_office_id = self.kwargs.get("pk")
        context["microsoft_office_key"] = get_object_or_404(
            models.MicrosoftOffice, pk=microsoft_office_id
        )
        return context


class MicrosoftOfficeAssignDetailView(UserAccessMixin, DetailView):
    model = models.MicrosoftOfficeAssignment


class MicrosoftOfficeAssignListView(UserAccessMixin, ListView):
    model = models.MicrosoftOfficeAssignment


class MicrosoftOfficeAssignUpdateView(UserAccessMixin, UpdateView):
    model = models.MicrosoftOfficeAssignment
    fields = "__all__"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
