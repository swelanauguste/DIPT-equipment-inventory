import csv
from datetime import datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.user_permission import UserAccessMixin

from . import forms, models


class ComputerListView(UserAccessMixin, ListView):
    model = models.Computer
    template_name = "computer_list.html"
    context_object_name = "computers"
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.none()  # Start with an empty queryset

        # Retrieve and apply filter parameters
        query = self.request.GET.get("query")
        computer_name = self.request.GET.get("computer_name")
        status = self.request.GET.get("status")
        model = self.request.GET.get("model")
        os = self.request.GET.get("os")
        location = self.request.GET.get("location")
        department = self.request.GET.get("department")
        user = self.request.GET.get("user")

        # Check if any filter parameter is provided
        if query or computer_name or status or model or os or location or department or user:
            queryset = models.Computer.objects.all()
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

    def export_to_csv(self, queryset):
        current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"computers_{current_date}.csv"
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "#",
                "Project",
                "Model",
                "Serial Number",
                "Status",
                "Operating System",
                "Location",
                "Department",
                "User",
                "Comments",
            ]
        )

        for index, computer in enumerate(queryset, start=1):
            writer.writerow(
                [
                    index,
                    computer.from_project,
                    computer.model.name.upper(),
                    computer.serial_number.upper(),
                    computer.status.name,
                    computer.os,
                    computer.location,
                    computer.department,
                    computer.user.last(),
                    computer.notes,
                ]
            )

        return response

    def get(self, request, *args, **kwargs):
        if "export" in request.GET:
            queryset = self.get_queryset()
            return self.export_to_csv(queryset)
        return super().get(request, *args, **kwargs)


class ComputerCreateView(UserAccessMixin, CreateView):
    model = models.Computer
    form_class = forms.ComputerForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerUpdateView(UserAccessMixin, UpdateView):
    model = models.Computer
    form_class = forms.ComputerForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerDetailView(UserAccessMixin, DetailView):
    model = models.Computer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.CommentCreateForm
        return context


@login_required
def add_comment_view(request, slug):
    computer = get_object_or_404(models.Computer, slug=slug)
    form = forms.CommentCreateForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.computer = computer
            if request.user.is_authenticated:
                comment.created_by = request.user
                comment.updated_by = request.user
            comment.save()
            return redirect("computer-detail", slug=slug)

    # If the form is not valid or the request method is not POST
    return render(
        request,
        "computers/computer_detail.html",
        {"object": computer, "form": form},
    )


class ComputerModelListView(UserAccessMixin, ListView):
    model = models.ComputerModel
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        maker = self.request.GET.get("maker", "")
        computer_type = self.request.GET.get("computer_type", "")
        # ram = self.request.GET.get("ram", "")
        # hdd = self.request.GET.get("hdd", "")

        # Filter by search query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(processor__icontains=search_query)
                | Q(ram__icontains=search_query)
                | Q(hdd__icontains=search_query)
            )

        # Filter by maker (Foreign)
        if maker:
            queryset = queryset.filter(maker_id=maker)

        # Filter by computer type
        if computer_type:
            queryset = queryset.filter(computer_type=computer_type)

        # # Filter by RAM
        # if ram:
        #     queryset = queryset.filter(ram=ram)

        # # Filter by HDD/Storage
        # if hdd:
        #     queryset = queryset.filter(hdd=hdd)

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


class ComputerModelCreateView(UserAccessMixin, CreateView):
    model = models.ComputerModel
    form_class = forms.ComputerModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelUpdateView(UserAccessMixin, UpdateView):
    model = models.ComputerModel
    form_class = forms.ComputerModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelDetailView(UserAccessMixin, DetailView):
    model = models.ComputerModel


class MonitorListView(UserAccessMixin, ListView):
    model = models.Monitor


class MonitorCreateView(UserAccessMixin, CreateView):
    model = models.Monitor
    form_class = forms.MonitorForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorUpdateView(UserAccessMixin, UpdateView):
    model = models.Monitor
    form_class = forms.MonitorForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorDetailView(UserAccessMixin, DetailView):
    model = models.Monitor


class MonitorModelListView(UserAccessMixin, ListView):
    model = models.MonitorModel
    paginate_by = 20


class MonitorModelCreateView(UserAccessMixin, CreateView):
    model = models.MonitorModel
    form_class = forms.MonitorModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorModelUpdateView(UserAccessMixin, UpdateView):
    model = models.MonitorModel
    form_class = forms.MonitorModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MonitorModelDetailView(UserAccessMixin, DetailView):
    model = models.MonitorModel
