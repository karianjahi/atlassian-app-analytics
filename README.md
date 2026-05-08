# Atlassian App Analytics

Customer Behaviour Analytics Platform for Atlassian Marketplace Apps.

## Overview

Atlassian App Analytics is a Django-based analytics prototype for understanding customer behaviour, product adoption, churn risk, and customer health for Atlassian Marketplace-style apps.

The project combines:

- Django backend
- Django REST Framework APIs
- PostgreSQL database
- HTML, CSS, and JavaScript frontend
- Chart.js visualizations
- pandas data preparation
- scikit-learn machine learning
- rule-based health scoring
- ML churn prediction
- historical health tracking
- automated alerts and insights

The goal is to demonstrate how product usage data can be transformed into actionable customer intelligence.

## Motivation

Atlassian Marketplace vendors often serve many customers across Jira and Confluence apps. As usage grows, product teams need ways to answer questions such as:

- Which customers are actively using the product?
- Which customers are at risk of churn?
- Which features are being adopted?
- Which customers need support or intervention?
- How is customer health changing over time?
- What might happen next?

This project simulates an analytics platform that helps answer these questions using event data, health scoring, machine learning, and interactive dashboards.

## Inspired by codefortynine

This project is inspired by the type of apps built by codefortynine GmbH, an Atlassian Marketplace vendor based in Karlsruhe.

The prototype is designed around the idea of analyzing customer behaviour for Atlassian cloud apps such as:

- Deep Clone for Jira
- External Data for Jira Fields
- Quick Filters for Jira Dashboards
- Merge Agent for Jira
- Snipe-IT for Jira

The project is not affiliated with codefortynine. It is a portfolio/demo project designed to show product thinking, backend engineering, frontend development, analytics, and applied machine learning.

## Key Features

### 1. Landing Page

The project includes a landing page that explains:

- background of the mini-project
- motivation
- connection to Atlassian Marketplace apps
- what the prototype does

### 2. API-driven Dashboard

The dashboard is rendered as an HTML shell and populated through JavaScript API calls.

It displays:

- total customers
- average health score
- healthy customers
- watch customers
- high-risk customers
- ML model accuracy
- customer health table
- health distribution doughnut chart
- feature importance table
- top ML churn-risk customers
- top rule-based risk customers

The customer health table uses pagination so only a limited number of rows are loaded at a time.

### 3. Customer Detail Page

Each customer has an API-driven detail page showing:

- customer profile
- app name
- country
- company size
- license tier
- installation date
- health metrics
- risk explanation
- recommended actions
- alerts
- automated insights
- health forecast
- event distribution chart
- events-over-time chart
- health history chart
- recent events table

### 4. Customer Health Scoring

Each customer receives a health score based on:

- usage score
- feature adoption score
- reliability score
- support score

The health score follows this weighted formula:

```text
health_score =
    α * usage_score +
    β * feature_adoption_score +
    γ * reliability_score +
    δ * support_score
```

The score is converted into risk labels:

```text
80–100 → Healthy
50–79  → Watch
0–49   → High Risk
```

### 5. Event Analytics

Customer behaviour is tracked using usage events such as:

```text
installed_app
configured_app
created_clone
used_dashboard_filter
connected_external_data_source
sync_failed
opened_support_ticket
subscription_cancelled
```

The app visualizes:

- event type distribution
- events over time
- recent events per customer

### 6. Machine Learning Churn Prediction

The project includes a machine learning pipeline using scikit-learn.

The model predicts churn probability using features such as:

- usage score
- feature adoption score
- reliability score
- support score
- company size

The project currently uses logistic regression for churn prediction.

The app stores:

- rule-based churn risk
- ML-based churn probability
- model accuracy
- feature importance

### 7. Feature Importance

The dashboard explains which features influence churn prediction.

Example interpretation:

```text
usage_score              → decreases churn risk
support_score            → increases churn risk
feature_adoption_score   → decreases churn risk
```

### 8. Health History

The system stores historical snapshots of customer health.

Each snapshot includes:

- usage score
- feature adoption score
- reliability score
- support score
- health score
- churn risk
- ML churn probability
- risk label
- timestamp

This allows the app to show customer health trends over time.

### 9. Automated Insights

The app generates plain-English insights from historical health data.

Example insights:

```text
Health score declined by 12.5 points over time.
ML churn probability increased by 18%.
Customer is currently in a high-risk health range.
```

### 10. Alerts

The platform generates alerts when customer risk signals become serious.

Example alerts:

```text
Health score dropped sharply.
ML churn probability increased significantly.
Customer is currently classified as high risk.
ML model predicts extremely high churn probability.
```

### 11. Forecasting

The project includes a simple health-score forecast based on recent historical trend.

Example:

```text
latest health score = 54
average recent change = -6
forecast next health score = 48
```

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### Data Science / Machine Learning

- pandas
- scikit-learn
- joblib

## Architecture

```text
PostgreSQL
   ↓
Django Models
   ↓
Analytics Services
   ↓
Machine Learning Pipeline
   ↓
Django REST API
   ↓
JavaScript Frontend
   ↓
Charts, Tables, Insights, Alerts
```

## Main Django Apps / Files

```text
analytics/
├── models.py
├── views.py
├── services.py
├── ml.py
├── serializers.py
├── templates/
│   └── analytics/
│       ├── landing_page.html
│       ├── dashboard.html
│       └── customer_detail.html
├── static/
│   └── analytics/
│       ├── css/
│       │   ├── landing_page.css
│       │   ├── dashboard.css
│       │   └── customer_detail.css
│       └── js/
│           ├── dashboard.js
│           └── customer_detail.js
└── management/
    └── commands/
        ├── update_customer_health.py
        └── update_ml_churn.py
```

## Core Models

### Customer

Represents a customer using an Atlassian Marketplace app.

### UsageEvent

Represents customer activity and product usage events.

### CustomerHealth

Stores the latest customer health metrics and churn risk.

### CustomerHealthSnapshot

Stores historical health snapshots over time.

## API Endpoints

Example endpoints:

```text
GET /api/customers/
GET /api/customers/<id>/
GET /api/customers/<id>/events/
GET /api/customers/<id>/health/
GET /api/customers/<id>/detail/
GET /api/customers/<id>/health-history/

GET /api/customer-health/
GET /api/summary/
GET /api/dashboard/

GET /api/ml/metrics/
GET /api/ml/feature-importance/
```

## Management Commands

Update rule-based customer health:

```bash
python manage.py update_customer_health
```

Update ML churn probabilities:

```bash
python manage.py update_ml_churn
```

Run both through the helper script:

```bash
./update_analytics.sh
```

## Bash Script

Example `update_analytics.sh`:

```bash
#!/bin/bash

echo "Updating customer health..."
python manage.py update_customer_health

echo "Updating ML churn probabilities..."
python manage.py update_ml_churn

echo "Analytics update complete."
```

## Running the Project

### 1. Clone repository

```bash
git clone https://github.com/your-username/atlassian-app-analytics.git
cd atlassian-app-analytics
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Update `settings.py` with your database credentials.

Example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "analytics_db",
        "USER": "postgres",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Start development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Demo Workflow

A typical demo flow:

1. Open the landing page.
2. Go to the dashboard.
3. Review customer health distribution.
4. Check risk rankings.
5. Open a customer detail page.
6. Review health metrics, alerts, insights, and forecasts.
7. Inspect event distribution and time-series charts.
8. Run update commands to refresh analytics and ML probabilities.

## Machine Learning Notes

This project demonstrates an end-to-end ML workflow:

```text
Django data
↓
pandas DataFrame
↓
scikit-learn model training
↓
model evaluation
↓
saved model with joblib
↓
predicted churn probabilities
↓
API + frontend display
```

The current model is intentionally simple and explainable.

## Limitations

This is a prototype and portfolio project.

Current limitations:

- Uses synthetic/demo customer data
- Uses synthetic churn labels based on health score threshold
- ML model is trained on limited data
- Forecasting uses a simple trend-based method
- No authentication/authorization layer yet
- No production deployment setup yet
- No real Atlassian API integration yet
- No real customer billing or cancellation data yet

In a production system, churn labels should come from real subscription outcomes such as cancellations, non-renewals, downgrades, or long-term inactivity.

## Future Improvements

Possible next steps:

- Real Atlassian API integration
- Authentication and user roles
- Customer search and filtering
- More robust pagination
- Better ML model evaluation
- Model retraining history
- Health trend anomaly detection
- Forecast confidence intervals
- Exportable CSV/PDF reports
- Deployment with Docker
- React frontend migration
- Scheduled jobs using cron or Celery

## Why This Project Matters

This project demonstrates the ability to combine:

- backend engineering
- REST API design
- frontend JavaScript rendering
- product analytics
- data modeling
- machine learning
- explainability
- forecasting
- customer success thinking

It is designed to show how raw product usage data can become actionable customer intelligence.

## Author

Dr. Joseph Njeri

Data scientist with experience in teaching, applied analytics, and building practical data products.

## License

MIT
