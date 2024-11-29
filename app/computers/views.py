from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import forms, models


class ComputerListView(LoginRequiredMixin, ListView):
    model = models.Computer
    template_name = "computer_list.html"
    context_object_name = "computers"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve and apply filter parameters
        query = self.request.GET.get("query")
        computer_name = self.request.GET.get("computer_name")
        status = self.request.GET.get("status")
        model = self.request.GET.get("model")
        os = self.request.GET.get("os")
        location = self.request.GET.get("location")
        department = self.request.GET.get("department")
        user = self.request.GET.get("user")

        if query:
            queryset = queryset.filter(
                Q(serial_number__icontains=query)
                | Q(computer_name__icontains=query)
                | Q(notes__icontains=query)
            )

        if status:
            queryset = queryset.filter(status__id=status)
        if model:
            queryset = queryset.filter(model__id=model)
        if os:
            queryset = queryset.filter(os__id=os)
        if location:
            queryset = queryset.filter(location__id=location)
        if department:
            queryset = queryset.filter(department__id=department)
        if user:
            queryset = queryset.filter(user__id=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filter dropdown options
        context["statuses"] = models.Status.objects.all()
        context["models"] = models.ComputerModel.objects.all()
        context["operating_systems"] = models.OperatingSystem.objects.all()
        context["locations"] = models.Location.objects.all()
        context["departments"] = models.Department.objects.all()
        context["users"] = models.User.objects.all()

        # Count total computers
        context["computer_count"] = self.get_queryset().count()

        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context


class ComputerCreateView(LoginRequiredMixin, CreateView):
    model = models.Computer
    form_class = forms.ComputerForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Computer
    form_class = forms.ComputerForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerDetailView(LoginRequiredMixin, DetailView):
    model = models.Computer


class ComputerModelListView(LoginRequiredMixin, ListView):
    model = models.ComputerModel
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        maker = self.request.GET.get("maker", "")
        computer_type = self.request.GET.get("computer_type", "")
        ram = self.request.GET.get("ram", "")
        hdd = self.request.GET.get("hdd", "")

        # Filter by search query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(processor__icontains=search_query)
            )

        # Filter by maker (Foreign)
        if maker:
            queryset = queryset.filter(maker_id=maker)

        # Filter by computer type
        if computer_type:
            queryset = queryset.filter(computer_type=computer_type)

        # Filter by RAM
        if ram:
            queryset = queryset.filter(ram=ram)

        # Filter by HDD/Storage
        if hdd:
            queryset = queryset.filter(hdd=hdd)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["computer_model_count"] = (
            self.get_queryset().count()
        )  # For maker dropdown
        context["makers"] = models.Maker.objects.all()  # For maker dropdown
        context["computer_types"] = (
            models.ComputerModel.computer_type_list
        )  # For computer type dropdown
        return context


class ComputerModelCreateView(LoginRequiredMixin, CreateView):
    model = models.ComputerModel
    form_class = forms.ComputerModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ComputerModel
    form_class = forms.ComputerModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelDetailView(LoginRequiredMixin, DetailView):
    model = models.ComputerModel


class MonitorListView(LoginRequiredMixin, ListView):
    model = models.Monitor


class MonitorCreateView(LoginRequiredMixin, CreateView):
    model = models.Monitor
    form_class = forms.MonitorForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Monitor
    form_class = forms.MonitorForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorDetailView(LoginRequiredMixin, DetailView):
    model = models.Monitor


class MonitorModelListView(LoginRequiredMixin, ListView):
    model = models.MonitorModel
    paginate_by = 20


class MonitorModelCreateView(LoginRequiredMixin, CreateView):
    model = models.MonitorModel
    form_class = forms.MonitorModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorModelUpdateView(LoginRequiredMixin, UpdateView):
    model = models.MonitorModel
    form_class = forms.MonitorModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorModelDetailView(LoginRequiredMixin, DetailView):
    model = models.MonitorModel


class MicrosoftOfficeListView(LoginRequiredMixin, ListView):
    model = models.MicrosoftOffice
    paginate_by = 20
    template_name = "computers/microsoft_office_unused_list.html"

    def get_queryset(self):
        # Filter the queryset to only include items where date_installed is None
        return models.MicrosoftOffice.objects.filter(date_installed__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_count"] = self.get_queryset().count()
        return context


class MicrosoftOfficeInstalledListView(LoginRequiredMixin, ListView):
    model = models.MicrosoftOffice
    paginate_by = 20
    template_name = "computers/microsoft_office_installed_list.html"

    def get_queryset(self):
        # Filter the queryset to only include items where date_installed is None
        return models.MicrosoftOffice.objects.filter(date_installed__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_count"] = self.get_queryset().count()
        return context


class MicrosoftOfficeDetailView(LoginRequiredMixin, DetailView):
    model = models.MicrosoftOffice


class MicrosoftOfficeCreateView(LoginRequiredMixin, CreateView):
    model = models.MicrosoftOffice
    form_class = forms.MicrosoftOfficeForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MicrosoftOfficeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.MicrosoftOffice
    form_class = forms.MicrosoftOfficeForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MicrosoftOfficeAssignView(LoginRequiredMixin, CreateView):
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


class MicrosoftOfficeAssignDetailView(LoginRequiredMixin, DetailView):
    model = models.MicrosoftOfficeAssignment


class MicrosoftOfficeAssignListView(LoginRequiredMixin, ListView):
    model = models.MicrosoftOfficeAssignment


class MicrosoftOfficeAssignUpdateView(LoginRequiredMixin, UpdateView):
    model = models.MicrosoftOfficeAssignment
    fields = "__all__"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
