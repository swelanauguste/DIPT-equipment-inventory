from django.urls import path

from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article-list"),
    path("detail/<slug:slug>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("create/", views.ArticleCreateView.as_view(), name="article-create"),
    path(
        "update/<slug:slug>/", views.ArticleUpdateView.as_view(), name="article-update"
    ),
]
