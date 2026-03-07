from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="HomePage"),
    path("posts", views.PostView.as_view(), name="Posts"),
    path("posts/<slug:slug>", views.BlogPageView.as_view(), name="BlogPage"),
    path("read-later", views.ReadLaterView.as_view(), name="readlater")
]