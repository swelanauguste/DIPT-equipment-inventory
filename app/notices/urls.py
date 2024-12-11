from django.urls import path

from . import views

urlpatterns = [
    path("", views.PublishedNoticeListView.as_view(), name="notice-published-list"),
    path("notice-list/", views.NoticeListView.as_view(), name="notice-list"),
    path("create/", views.NoticeCreateView.as_view(), name="notice-create"),
    path("<slug:slug>/", views.NoticeDetailView.as_view(), name="notice-detail"),
    path("update/<slug:slug>/", views.NoticeUpdateView.as_view(), name="notice-update"),
    path("publish/<slug:slug>/", views.notice_publish_view, name="notice-publish"),
    path(
        "unpublish/<slug:slug>/", views.notice_unpublish_view, name="notice-unpublish"
    ),
]
