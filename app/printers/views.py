from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import forms, models


class PrinterListView(LoginRequiredMixin, ListView):
    model = models.Printer
    context_object_name = "printers"
    paginate_by = 20  # Number of items per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(serial_number__icontains=search_query)
                | Q(printer_name__icontains=search_query)
                | Q(model__name__icontains=search_query)
                | Q(location__name__icontains=search_query)
                | Q(department__name__icontains=search_query)
                | Q(status__name__icontains=search_query)
                | Q(ip_addr__icontains=search_query)
            )

        # Filtering by fields
        model_id = self.request.GET.get("model")
        if model_id:
            queryset = queryset.filter(model_id=model_id)

        location_id = self.request.GET.get("location")
        if location_id:
            queryset = queryset.filter(location_id=location_id)

        department_id = self.request.GET.get("department")
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        status_id = self.request.GET.get("status")
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include filtering options in the context
        context["printer_count"] = self.get_queryset().count()
        context["models"] = models.PrinterModel.objects.all()
        context["locations"] = models.Location.objects.all()
        context["departments"] = models.Department.objects.all()
        context["statuses"] = models.Status.objects.all()
        return context


class PrinterCreateView(LoginRequiredMixin, CreateView):
    model = models.Printer
    form_class = forms.PrinterForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterDetailView(LoginRequiredMixin, DetailView):
    model = models.Printer


class PrinterUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Printer
    fields = "__all__"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelListView(LoginRequiredMixin, ListView):
    model = models.PrinterModel

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(maker__name__icontains=search_query)
            )

        # Filtering by fields
        maker_id = self.request.GET.get("maker")
        if maker_id:
            queryset = queryset.filter(maker_id=maker_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include filtering options in the context
        context["printer_model_count"] = self.get_queryset().count()
        context["makers"] = models.Maker.objects.all()
        return context


class PrinterModelCreateView(LoginRequiredMixin, CreateView):
    model = models.PrinterModel
    form_class = forms.PrinterModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelDetailView(LoginRequiredMixin, DetailView):
    model = models.PrinterModel


class PrinterModelUpdateView(LoginRequiredMixin, UpdateView):
    model = models.PrinterModel
    fields = "__all__"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
