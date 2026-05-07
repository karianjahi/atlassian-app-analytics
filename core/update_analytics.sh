#!/bin/bash

echo "Updating customer health..."

python manage.py update_customer_health

echo "Updating ML churn probabilities..."

python manage.py update_ml_churn

echo "Analytics update complete."