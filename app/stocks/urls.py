from django.urls import path

from .views import ItemDetailView, ItemListView, TransactionCreateView, ItemCreateView

urlpatterns = [
    path("", ItemListView.as_view(), name="stock-list"),
    path("stock/<int:pk>/", ItemDetailView.as_view(), name="stock-detail"),
    path(
        "transactions/add", TransactionCreateView.as_view(), name="stock-transaction"
    ),
    path("create/", ItemCreateView.as_view(), name="stock-create"),
]
