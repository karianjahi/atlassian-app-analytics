from django.urls import path

from . import views


urlpatterns = [
    # Page views
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "customers/<int:customer_id>/",
        views.customer_detail,
        name="customer_detail",
    ),
    path("upload-csv/", views.upload_csv, name="upload_csv"),

    # API endpoints
    path("api/customers/", views.customer_list_api, name="customer_list_api"),
    path(
        "api/customers/<int:customer_id>/",
        views.customer_detail_api,
        name="customer_detail_api",
    ),
    path(
        "api/customers/<int:customer_id>/health/",
        views.customer_health_api,
        name="customer_health_api",
    ),
    path(
        "api/customers/<int:customer_id>/events/",
        views.customer_events_api,
        name="customer_events_api",
    ),
    path(
        "api/customers/<int:customer_id>/detail/",
        views.customer_detail_data_api,
        name="customer_detail_data_api",
    ),
    path(
        "api/customers/<int:customer_id>/health-history/",
        views.customer_health_history_api,
        name="customer_health_history_api",
    ),
    path(
        "api/customer-health/",
        views.customer_health_list_api,
        name="customer_health_list_api",
    ),
    path(
        "api/summary/",
        views.summary_api,
        name="summary_api",
    ),
    path(
        "api/dashboard/",
        views.dashboard_data_api,
        name="dashboard_data_api",
    ),
    path(
        "api/ml/metrics/",
        views.ml_model_metrics_api,
        name="ml_model_metrics_api",
    ),
    path(
        "api/ml/feature-importance/",
        views.ml_feature_importance_api,
        name="ml_feature_importance_api",
    ),
]