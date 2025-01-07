from django.urls import path

from .views import (
    ItemCreateView,
    ItemDetailView,
    ItemListView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionListView,
)

urlpatterns = [
    path("", ItemListView.as_view(), name="stock-list"),
    path("stock/<slug:slug>/", ItemDetailView.as_view(), name="stock-detail"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/add", TransactionCreateView.as_view(), name="stock-transaction"),
    path(
        "stock/<slug:slug>/transactions/add/",
        TransactionCreateView.as_view(),
        name="stock-transaction-add",
    ),
    path(
        "transactions/<int:pk>/", TransactionDetailView.as_view(), name="trans-detail"
    ),
    path("create/", ItemCreateView.as_view(), name="stock-create"),
]
