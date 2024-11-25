from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import forms, models


class ComputerListView(LoginRequiredMixin, ListView):
    model = models.Computer
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get query parameters
        serial_number = self.request.GET.get("serial_number")
        computer_name = self.request.GET.get("computer_name")
        status = self.request.GET.get("status")
        model = self.request.GET.get("model")
        os = self.request.GET.get("os")
        location = self.request.GET.get("location")
        department = self.request.GET.get("department")
        date_received = self.request.GET.get("date_received")
        date_installed = self.request.GET.get("date_installed")
        user = self.request.GET.get("user")

        # Apply filters
        if serial_number:
            queryset = queryset.filter(serial_number__icontains=serial_number)
        if computer_name:
            queryset = queryset.filter(computer_name__icontains=computer_name)
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
        if date_received:
            queryset = queryset.filter(date_received=date_received)
        if date_installed:
            queryset = queryset.filter(date_installed=date_installed)
        if user:
            queryset = queryset.filter(user__id=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass related field data to the template
        context["statuses"] = models.Status.objects.all()
        context["models"] = models.ComputerModel.objects.all()
        context["operating_systems"] = models.OperatingSystem.objects.all()
        context["locations"] = models.Location.objects.all()
        context["departments"] = models.Department.objects.all()
        context["users"] = models.User.objects.all()
        context["computer_count"] = models.Computer.objects.all().count()
        

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

        # Filter by maker (ForeignKey)
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
