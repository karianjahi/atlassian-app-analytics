# Atlassian App Analytics

Customer Behaviour Analytics Platform for Atlassian Marketplace Apps
(Jira & Confluence)

## Overview

This project is a full-stack analytics platform designed to help
Atlassian Marketplace vendors understand how customers interact with
their apps.

It focuses on: - Customer activation and onboarding - Feature adoption -
Usage patterns - Customer health scoring - Churn risk detection

The goal is to provide actionable insights that help product teams
improve retention, prioritize features, and identify struggling
customers early.

## Motivation

Atlassian Marketplace apps serve thousands of companies with very
different usage patterns. However, raw event data alone is not
sufficient to answer key product questions:

-   Which customers are successfully adopting the app?
-   Where do users drop off in the onboarding process?
-   Which features drive long-term retention?
-   Which customers are at risk of churning?

This project demonstrates how data science and backend engineering can
be combined to build a practical analytics tool for answering these
questions.

## Features

### 1. Customer Dashboard

-   Total customers
-   Active users (last 30 days)
-   Trial-to-paid conversion (simulated)
-   Average health score
-   High-risk customers overview

### 2. Activation Funnel

Tracks customer progression: - App installed - App configured - First
successful usage - Repeated usage - (Simulated) conversion to paid

### 3. Customer Health Score

Each customer is scored based on:

-   Usage frequency
-   Feature adoption
-   Reliability (error rates)
-   Support interaction

Health score formula:

health_score = α \* usage_score + β \* feature_adoption_score + γ \*
reliability_score + δ \* support_score

Labels: - 80--100 → Healthy - 50--79 → Watch - 0--49 → High Risk

### 4. Churn Risk Prediction

A machine learning model (Random Forest) predicts churn risk using:

-   Recency of activity
-   Number of events (last 30 days)
-   Error frequency
-   Support ticket count
-   Feature diversity
-   Company size

### 5. Customer Detail View

Per-customer insights: - Usage timeline - Feature adoption - Errors and
failures - Support activity - Risk explanation - Suggested actions

### 6. Feature Usage Analytics

-   Most used features
-   Underutilized features
-   Power-user patterns

### 7. CSV Data Upload

Upload event data in CSV format:

customer_id, company_name, country, company_size, license_tier,
app_name, event_type, timestamp

## Tech Stack

-   Backend: Django
-   Database: PostgreSQL
-   Data Processing: pandas
-   Machine Learning: scikit-learn
-   Frontend: HTML, CSS, JavaScript
-   Visualization: Chart.js

## Architecture

Django (views + templates) \| \|-- pandas (data aggregation) \|--
scikit-learn (churn model) \| PostgreSQL (customers + events)

## Data Model

### Customer

-   company_name
-   country
-   company_size
-   license_tier
-   app_name
-   installed_at

### UsageEvent

-   customer (FK)
-   event_type
-   timestamp
-   metadata (JSON)

### CustomerHealth

-   usage_score
-   feature_adoption_score
-   reliability_score
-   support_score
-   health_score
-   churn_risk
-   risk_label

## Example Events

installed_app configured_app created_clone used_dashboard_filter
connected_external_data_source sync_failed opened_support_ticket
subscription_cancelled

## Running the Project

### 1. Clone repository

git clone https://github.com/karianjahi/atlassian-app-analytics.git
cd atlassian-app-analytics

### 2. Create virtual environment

python -m venv venv source venv/bin/activate \# Linux / macOS
venv`\Scripts`{=tex}`\activate      `{=tex}\# Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure PostgreSQL

Update `settings.py`:

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql',
'NAME': 'analytics_db', 'USER': 'postgres', 'PASSWORD': 'yourpassword',
'HOST': 'localhost', 'PORT': '5432', } }

### 5. Run migrations

python manage.py makemigrations python manage.py migrate

### 6. Load sample data (optional)

python manage.py shell \>\>\> from analytics.services import
generate_demo_data \>\>\> generate_demo_data()

### 7. Start server

python manage.py runserver

Open: http://127.0.0.1:8000/

## Machine Learning

The churn model is implemented using:

sklearn.ensemble.RandomForestClassifier

Feature engineering is done using pandas aggregation pipelines.

This is a demo model trained on synthetic data, designed to
illustrate: - feature engineering - model integration in a web app -
real-world product analytics use cases

## Privacy Considerations

This project is designed with privacy in mind: - No personally
identifiable user data is required - All analytics are based on
aggregated, anonymized usage events

## Future Improvements

-   Integration with Atlassian APIs (Forge / REST)
-   Real-time event streaming
-   Advanced cohort analysis
-   A/B testing insights
-   Role-based dashboards
-   Exportable reports

## Why This Project

This project demonstrates: - Full-stack development with Django - Data
processing with pandas - Applied machine learning with scikit-learn -
Product-oriented thinking - Real-world SaaS analytics use cases

It is designed as a prototype for analytics systems used by Atlassian
Marketplace vendors.

## Author

Data Scientist with 5+ years experience in teaching and applied
analytics, focused on building practical, production-oriented tools that
connect data insights with product decisions.

## License

MIT
