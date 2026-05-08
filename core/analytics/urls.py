from django.urls import path
from .import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("customers/<int:customer_id>/", views.customer_detail, name="customer_detail"),
    
    
    ## api urls
    path("api/customers/", views.customer_list_api),
    path("api/customers/<int:customer_id>/", views.customer_detail_api),
    path("api/customers/<int:customer_id>/health/", views.customer_health_api),
    path("api/customers/<int:customer_id>/events/", views.customer_events_api),
    path("api/customer-health/", views.customer_health_list_api),
    path("api/summary", views.summary_api),
    path("api/dashboard/", views.dashboard_data_api),
    path("api/customers/<int:customer_id>/detail/", views.customer_detail_data_api, name="customer_detail_data_api"),
    path("api/ml/metrics/", views.ml_model_metrics_api),
    path("api/ml/feature-importance/", views.ml_feature_importance_api),
    path("api/customers/<int:customer_id>/health-history", views.customer_health_history_api)
]

