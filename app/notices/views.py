from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.user_permission import UserAccessMixin

from . import forms, models


class NoticeListView(UserAccessMixin, ListView):
    model = models.Notice
    template_name = "notices/notice_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("priority")
        draft = self.request.GET.get("draft")
        query = self.request.GET.get("notice", "")

        if draft == "1":
            queryset = queryset.filter(draft=True)
        if draft == "0":
            queryset = queryset.filter(draft=False)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(message__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options for dropdowns
        context["notice_count"] = self.get_queryset().count()

        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)

        return context


class PublishedNoticeListView(ListView):
    model = models.Notice
    template_name = "notices/published_list.html"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(expiration_date__gte=timezone.now())
            .filter(draft=False)
            .order_by("priority")
        )

        query = self.request.GET.get("notice", "")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(message__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options for dropdowns
        context["notice_count"] = self.get_queryset().count()
        # Preserve query parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop(
                "page"
            )  # Remove 'page' from query parameters to prevent duplication
        context["query_params"] = urlencode(query_params)
        return context


class NoticeCreateView(UserAccessMixin, CreateView):
    model = models.Notice
    form_class = forms.NoticeCreateForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class NoticeUpdateView(UserAccessMixin, UpdateView):
    model = models.Notice
    form_class = forms.NoticeCreateForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class NoticeDetailView(UserAccessMixin, DetailView):
    model = models.Notice


@login_required
def notice_publish_view(request, slug):
    notice = get_object_or_404(models.Notice, slug=slug)
    notice.draft = False
    notice.save()
    return redirect("notice-detail", slug=slug)


@login_required
def notice_unpublish_view(request, slug):
    notice = get_object_or_404(models.Notice, slug=slug)
    notice.draft = True
    notice.save()
    return redirect("notice-detail", slug=slug)
