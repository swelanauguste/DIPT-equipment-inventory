from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.user_permission import UserAccessMixin

from . import forms, models


class PrinterListView(UserAccessMixin, ListView):
    model = models.Printer
    context_object_name = "printers"
    paginate_by = 100  # Number of items per page

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


class PrinterCreateView(UserAccessMixin, CreateView):
    model = models.Printer
    form_class = forms.PrinterForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterDetailView(UserAccessMixin, DetailView):
    model = models.Printer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments_form"] = forms.CommentCreateForm
        return context


class PrinterUpdateView(UserAccessMixin, UpdateView):
    model = models.Printer
    form_class = forms.PrinterForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelListView(UserAccessMixin, ListView):
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


class PrinterModelCreateView(UserAccessMixin, CreateView):
    model = models.PrinterModel
    form_class = forms.PrinterModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelDetailView(UserAccessMixin, DetailView):
    model = models.PrinterModel


class PrinterModelUpdateView(UserAccessMixin, UpdateView):
    model = models.PrinterModel
    form_class = forms.PrinterModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@login_required
def add_comment_view(request, slug):
    printer = get_object_or_404(models.Printer, slug=slug)

    if request.method == "POST":
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.printer = printer
            if request.user.is_authenticated:
                comment.created_by = request.user
                comment.updated_by = request.user
            comment.save()
            return redirect("printer-detail", slug=slug)

    # If the form is not valid or the request method is not POST
    return render(
        request,
        "printer/printer_detail.html",
        {"printer": printer, "comment_form": form},
    )
