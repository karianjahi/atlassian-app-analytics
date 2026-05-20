# 🚀 Atlassian App Analytics

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-yellow?logo=javascript)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-orange)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-f7931e?logo=scikitlearn)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Railway](https://img.shields.io/badge/Deployment-Railway-0B0D0E?logo=railway)
![REST API](https://img.shields.io/badge/API-Django_REST_Framework-red)
![WhiteNoise](https://img.shields.io/badge/Static-WhiteNoise-purple)
![Status](https://img.shields.io/badge/Status-Live-success)

Customer Behaviour Analytics Platform for Atlassian Marketplace Apps.

> **Live Demo:** [customer health](https://customerhealth-atlassian-app-analytics.up.railway.app/upload-csv/)  
> **GitHub Repository:** [atlassian app analytics](https://github.com/karianjahi/atlassian-app-analytics)

## 📖 Overview

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
- CSV upload and validation
- upload audit logging
- duplicate detection
- trend-based forecasting
- cloud deployment on Railway

The goal is to demonstrate how product usage data can be transformed into actionable customer intelligence.

## 🏢 Motivation

Atlassian Marketplace vendors often serve many customers across Jira and Confluence apps. As usage grows, product teams need ways to answer questions such as:

- Which customers are actively using the product?
- Which customers are at risk of churn?
- Which features are being adopted?
- Which customers need support or intervention?
- How is customer health changing over time?
- What might happen next?

This project simulates an analytics platform that helps answer these questions using event data, health scoring, machine learning, and interactive dashboards.

## 💡 Inspired by codefortynine GmbH

This project is inspired by the type of apps built by codefortynine GmbH, an Atlassian Marketplace vendor based in Karlsruhe.

The project is not affiliated with codefortynine. It is a portfolio/demo project designed to show product thinking, backend engineering, frontend development, analytics, and applied machine learning.

## ✨ Key Features

### 🏠 Landing Page
- Project overview and motivation
- Architecture summary
- Navigation to dashboard and CSV upload

### 📂 CSV Upload and Data Ingestion
- Browser-based CSV upload
- Schema validation
- Mandatory `installed_at` column
- Customer creation and reuse
- Usage event ingestion
- Duplicate event detection
- Automatic analytics refresh
- Success summary
- Processing indicator

### 📜 Upload Audit Logging
Every upload is recorded in `CSVUploadLog` with:
- Filename
- Upload timestamp
- Customers created
- Events imported
- Duplicates skipped
- Invalid rows skipped
- Processing status

### 📊 API-driven Dashboard
- Total customers
- Average health score
- Healthy / Watch / High Risk counts
- ML model accuracy
- Customer health table
- Health distribution chart
- Feature importance
- Top ML churn-risk customers
- Top rule-based risk customers
- Pagination

### 👤 Customer Detail Page
- Customer profile
- Health metrics
- Risk explanation
- Recommended actions
- Alerts
- Automated insights
- Forecast
- Event charts
- Health history chart
- Recent events

### 📈 Customer Health Scoring
Weighted score based on:
- Usage
- Feature adoption
- Reliability
- Support

### 📊 Rule-Based Churn Risk
`churn_risk = 100 - health_score`

### 🤖 Machine Learning Churn Prediction
- Logistic Regression
- Synthetic churn labels
- Model accuracy
- Feature importance
- Model persistence with `joblib`

### 📜 Historical Snapshots
- Component scores
- Health score
- Risk label
- Churn probability
- Timestamp

### 💬 Automated Insights
Narrative summaries of customer trends.

### 🚨 Alerts
Automatic detection of sharp deterioration.

### 🔮 Forecasting
Projects the next health score using recent historical trends.

### 🔍 Filtering and Sorting APIs
Examples:
- `/api/customer-health/?risk_label=high_risk`
- `/api/customer-health/?ordering=-support_score`
- `/api/customers/?country=Germany`

### 🧪 Synthetic Data Generation
Demo data and large CSV generators.

### 🌐 Deployment on Railway
- PostgreSQL
- Gunicorn
- WhiteNoise
- Environment variables
- Automated migrations and static collection

## 🛠️ Tech Stack

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

### Deployment
- Railway
- Gunicorn
- WhiteNoise

## 🏗️ Architecture

```text
CSV Upload / Synthetic Data
           ↓
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

## 📂 Main Django Apps / Files

```text
analytics/
├── models.py
├── views.py
├── services.py
├── ml.py
├── serializers.py
├── forms.py
├── templates/
│   └── analytics/
│       ├── landing_page.html
│       ├── dashboard.html
│       ├── customer_detail.html
│       └── upload_csv.html
├── static/
│   └── analytics/
│       ├── css/
│       └── js/
└── management/
    └── commands/
        ├── update_customer_health.py
        └── update_ml_churn.py
```

## 🧱 Core Models
- Customer
- UsageEvent
- CustomerHealth
- CustomerHealthSnapshot
- CSVUploadLog

## 📡 API Endpoints

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

## ⚙️ Management Commands

```bash
python manage.py update_customer_health
python manage.py update_ml_churn
./update_analytics.sh
```

## 🚀 Running the Project

```bash
git clone https://github.com/karianjahi/atlassian-app-analytics.git
cd atlassian-app-analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🎬 Demo Workflow

1. Open the landing page.
2. Upload a CSV file.
3. Review the upload summary.
4. Open the dashboard.
5. Inspect health distribution and risk rankings.
6. Open a customer detail page.
7. Review alerts, insights, and forecasts.

## 🧠 Machine Learning Notes

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

## 🔐 Environment Variables
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- DATABASE_URL

## 🗃️ Admin Interface
- Customers
- Usage events
- Customer health
- Health snapshots
- CSV upload logs

## 🏛️ Decision-Support Questions

The application answers:

- What is customer health now?
- Which customers are likely to churn?
- Why is churn risk increasing?
- What actions should we take?
- Is intervention urgent?
- What may happen next?

## ⚠️ Limitations
- Uses synthetic/demo data
- Synthetic churn labels
- Simple forecasting
- No authentication yet
- No real Atlassian API integration

## 🔮 Future Improvements
- Real Atlassian API integration
- Authentication and user roles
- Better ML evaluation
- Forecast confidence intervals
- PDF/CSV exports
- Docker and CI/CD
- Scheduled jobs with Celery

## 🎯 Why This Project Matters

This project demonstrates:
- Backend engineering
- REST API design
- Frontend JavaScript
- Product analytics
- Data modeling
- Machine learning
- Explainability
- Forecasting
- Cloud deployment
- Auditability

## 🏆 Portfolio Significance

This is not merely a CRUD application. It demonstrates:
- Full-stack engineering
- Applied machine learning
- Customer success intelligence
- Production-style deployment
- Decision-support design

## 👨‍💻 Author

**Dr. Joseph Njeri**

Data scientist with experience in teaching, applied analytics, and building practical data products.

## 📄 License

MIT
