from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from . import forms, models


class ComputerListView(LoginRequiredMixin, ListView):
    model = models.Computer


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
