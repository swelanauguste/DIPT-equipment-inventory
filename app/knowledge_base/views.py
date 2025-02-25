from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.user_permission import UserAccessMixin

from .models import Article


class ArticleListView(UserAccessMixin, ListView):
    model = Article


class ArticleDetailView(UserAccessMixin, DetailView):
    model = Article


class ArticleCreateView(UserAccessMixin, CreateView):
    model = Article
    fields = ["title", "file", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UserAccessMixin, UpdateView):
    model = Article
    fields = ["title", "content"]
