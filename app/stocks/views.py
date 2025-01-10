from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import ItemForm
from .models import Item, Transaction


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy(
        "stock-list"
    )  # Redirect to the list of items after adding

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("stock", "")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(sku__icontains=query)
                | Q(category__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ["item", "transaction_type", "quantity", "notes"]
    success_url = reverse_lazy("stock-list")

    def get_initial(self):
        initial = super().get_initial()
        item_slug = self.kwargs.get("slug")
        if item_slug:
            item = get_object_or_404(Item, slug=item_slug)
            initial["item"] = item
        return initial

    def form_valid(self, form):
        form.instance.performed_by = self.request.user
        return super().form_valid(form)


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("transactions", "")

        if query:
            queryset = queryset.filter(
                Q(item__name__icontains=query)
                | Q(item__description__icontains=query)
                | Q(item__sku__icontains=query)
                | Q(item__category__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context
