from django.urls import path
from .import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.dashboard, name="dashboard"),,
    path("customers/<int:customer_id>/", views.customer_detail, name="customer_detail")
]

