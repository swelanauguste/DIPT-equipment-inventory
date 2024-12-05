from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments_form"] = forms.CommentCreateForm
        return context



def add_comment_view(request, slug):
    computer = get_object_or_404(models.Computer, slug=slug)

    if request.method == "POST":
        form = forms.CommentCreateForm(request.POST)
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
        request, "computer/computer_detail.html", {"computer": computer, "comment_form": form}
    )


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
