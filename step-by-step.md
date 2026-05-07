Steps
- Create a github project and clone it to your local repo
- Inside the local repo, create a virtual environment: `python -m venv venv`
- Upgrade `pip`. `pip install --upgrade pip`
- Activate the virtual environment `source venv/bin/activate`
- Install dependencies in the virtual environment: `Django`, `pandas`, `scikit-learn`, `gunicorn`, `psycopg2-binary`
- Create the requirements.txt file  using the command: `pip freeze > requirements.txt`
- Install postgresql for ubuntu:
    - `sudo apt update`
    - `sudo apt install postgresql postgresql-contrib`
    - `psql --version`
    - `sudo systemctl start postgresql.service`
    - You could then use the role associated with the current user by typing:
        - `sudo -i -u postgres`
        - To access the Postgres prompt and interact with it, run:
            - `psql`
        - To get back to postgres linux command prompt, run:
            - `\q`
        - To return to the regular system user, run
            - `exit`
    - You could log in to the postgres prompt directly by running the command:
        - `sudo -u postgres psql`
    - More information about postgres and how to create roles can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04).

- Set up the postgresql database for Django.
    - Log into a psql session:
        - `sudo -u postgres psql`
    - Create a database for your project
        - `CREATE DATABASE atlassian`;
    - Create a database user for our project with a password
        - `CREATE USER karianjahi WITH PASSWORD 'JahyeT7?Tem';`
    - Set default character encoding to UTF-8 and the default transaction isolation scheme to `read committed` which blocks reads from unauthorised transactions. Finally, set the timezone. By default, we use UTC.
        - `ALTER ROLE karianjahi SET client_encoding TO 'utf8';`
        - `ALTER ROLE karianjahi SET default_transaction_isolation TO 'read committed';`
        - `ALTER ROLE karianjahi SET timezone TO 'UTC';`
    - Finally give the new user access privileges to administer the new database
        - `GRANT ALL PRIVILEGES ON DATABASE atlassian TO karianjahi;`
    - Postgres is now set up so that Django can connect to it and do any transactions with the database.
    - To configure database access, use the `core/settings.py` file and find the databases section. The default database is `SQlite`. We don't need this anymore since we have configured our postgres. Guide django to use `psycopg2` adapter, change the database name, user and user password and specify where the database is located in the computer
`                                            . . .

                                        DATABASES = {
                                            'default': {
                                                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                                                'NAME': 'atlassian',
                                                'USER': 'karianjahi',
                                                'PASSWORD': 'JahyeT7?Tem',
                                                'HOST': 'localhost',
                                                'PORT': '',
                                            }
                                        }

                                        . . .`
- Finally, indicate where `static` files should be placed.   
    - `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`
    - `import os`
    - `STATIC_ROOT = os.path.join(BASE_DIR, 'static/')`
- Create the Django project: `django-admin startproject core`
- `cd core`
- Inside the core folder, create the analytics app: `python manage.py startapp analytics`
- Register the app in `core/settings.py`:
```bash
INSTALLED_APPS = [
    ...
    'analytics',
]
```
- Create the database models:

    **Customer Model**: This represents the company using the Jira App
    - columns: `company_name`, `country`, `company_size`, `license_tier`, `app_name`, `installed_at`, `created_at`

    **UsageEvent model**
    - columns: `customer id` (foreign key), `event_type`, `timestamp`, `metadata`, `created_at`
 

- Migrate the initial database schema to our PostgresSQL database using the `manage.py`
    - `pip manage.py makemigrations`
    - `pip manage.py migrate`
        - If it returns errors, you run the command: `ALTER DATABASE <database> OWNER TO <owner>;`
    - At this stage, tables have been created
    - You can always login to the postgres shell and type: 
        - `\l` - to see all databases
        - `\c <database>` to connect to the database you created
        - `\dt` to see the tables created
        - `SELECT * FROM <table>` To see the columns of the table

- To view the database in the admin panel, add the following to the analytics/admin.py
    - `from django.contrib import admin`
    - `from .models import Customer`
    - `admin.site.register(Customer)`
    - `admin.site.register(UsageEvent)`
    - `admin.site.register(CustomerHealth)`
- Create an administrative user for the project
    - `python manage.py createsuperuser`
        - user -> karianjahi or default
        - email -> any valid email. j@j.com
        - password: Sahel678
- Run the server locally by running: `python manage.py runserver`
- Go to `http://127.0.0.1:8000/admin` and create objects manually
- To run python scripts in django from the root, you must create a directory under the app known as management and a subdirectory called commands where you put all the scripts you need to interact with the database
- To automatically generate instances in the database, I create the file `analytics/management/commands/generate_<model>.py` by first creating those directories and then the file.
    - Remember that for the script to run you must load the `BaseCommand` which must sit at the top of any script
        `from django.core.management.base import BaseCommand`
    - The script must have a handle function. If you want to return something, you must use `stdout.write` for strings. If what you return is not a string, you must convert it to one. See the example below
    
```bash
from django.core.management.base import BaseCommand
from analytics.models import Customer, CustomerHealth, UsageEvent

# Get all Customer objects equivalent to SELECT * FROM customer
class Command(BaseCommand):
    help = "Interacting with the database"
    def handle(self, *args, **kwargs):
        all_customers = Customer.objects.all()
        self.stdout.write(str(all_customers))

```
                
    - Run the command `python manage.py generate_<model>` without `.py` extension to generate them
- You can always run `sudo -u postgres psql` and query the database `atlassian_db` for each of these tables
    - `\c atlassian_db` - connect to the table
    - `\dt` -> See the tables
    - `SELECT * FROM <analytics_<table-name>;`

- Create the health scoring logic using a new file `analytics/services.py`
- Calculate the health score for all customer in the `analytics/services.py`
- Create views for customer health. This accepts requests from server side.
- Create URLs for the view
- Include the app urls to the project urls
- Create templates folder and add a `dashboard.html` file in the analytics folder as follows:
    `analytics/templates/analytics/dashboard.html`
- Update the dashboard.html using context from views
- Use canvas to draw a doughnut
- Create static folder and add a `dashboard.js` under `analytics/static/analytics/js` and `dashboard.css` under `analytics/static/analytics/css`

- Create the Customer detail page
    - We want to have each customer clickable so we can inspect:
        - company profile
        - app name
        - health score
        - usage score
        - feature adoption score
        - reliability score
        - support score
        - churn risk
        - recent events
            - Create customer detail URL
            - Create customer_detail view
            - Create customer_detail.html
            - Link each customer row from dashboard table
            -  Display recent usage events

    - Start by creating a customer_detail function in views. The function extracts the customer from database, gets her health from inverse relationship with `CustomerHealth` (`related_name="health"`) and all usage events through the inverse relationship (`related_name="usage_events"`)
    - Then add a path for this view in `analytics.urls`
    - Create a customer_detail.html page 
        - The page just displays customer data plus the table
            - shows the customer properties, health and recent events
    - To interact with the shell, run `python manage.py shell`
        - to fake a request for the detail page, run;
        ```python
        from analytics.views import Customer
        from django.test import RequestFactory
        factory=RequestFactory()
        customer=Customer.objects.first()
        request = factory.get(f"/customer/{customer.id}")
        response=customer_detail(request, customer.id)
        print(response)
        ```
- Add functionality for creating a bar graph using a js file which is then imported as a static file
- Add functionality to include a time series
- Add chart styling and tooltips
- Add functionality to select time ranges and create a drop-down menu for this

- Add risk a explanation function in `services.py` and call it in views to display on web page
- Same for recommended actions

- To avoid making computations every time a request is made, we create a `update_customer_healthy.py` that runs manually for now (cron job later).

- The rest of the work is mainly on making the UI better looking and also to add a landing page.

# API Layer
- “I built a customer analytics system and exposed the insights via a REST API for integration with other frontends.”
- We use django-restframework. 
    - Add rest_framework under installed apps in settings
    - create a `serializers.py` file that serializes (or translates) the 3 models into JSON

- Create customer view `views.py`
    - Customer list: serialize all customers into JSON using the function `customer_list_api.py`
    - Customer detail: `customer_detail_api.py` 
    - Make sure urls.py reflect the various endpoints

- Create health view
    - Create a health view for each customer using the function `customer_health_api.py`

- Create events view
    - Create similarly the function `customer_events_api` and update `urls.py`

- Create all customer health records API
    - Create the function `customer_health_list_api`
    - The function is such that it accepts a risk label parameter from request as in `/api/customer-health/?risk_label=high_risk` so that it can filter records based on high_risk. Try filtering for `healthy` and `watch`.
- Also create functionality to filter customer api by country
- Sorting customer health API list results based on a parameter e.g. support score. Remember, `if .../?ordering=-support_score` (see the negative), we order from highest value to smallest.
- Create a summary endpoint for total_customers, average_health, healthy, watch and high_risk

- Next is to use API instead of Django templates (Decoupling frontend from Django templates)
- We do this by creating api endpoints.

- After ensuring our app is api-endpoint based, we can then move on to machine learning
Customer data

↓

Feature extraction

↓

Train ML model

↓

Predict churn probability

↓

Store prediction

↓

Show in dashboard

- Before training, we need `features + target`

## Features
- To predict churn, we need:
    - usage score
    - feature_adoption_score
    - reliability_score
    - support_score
    - company_size
    - license_tier
    - event_frequency

- Target: 
    - `did_churn = 1` 
    - `did_not_churn = 0`

- Since there are no real churn labels, we simulate them using existing risk logic

- We add a training label field in the `CustomerHealth` model called `did_churn`

- We create synthetic training labels for `did_churn` as follows:
    - `health.did_churn = health.health_score < 40`
    - In actual training data, churn labels comes actual churns from customers
    - Real churn labels usually come from:
        - Subscription cancellation
        - customer canceled subscription
        - License not renewed
        - renewal failed
        - Long inactivity
        - no usage for 90 days
        - Downgrade behavior
        - enterprise → free tier
 
 - At this stage, we now have
    - `X = features`
    - `y = target`

- Once we have this, we can:
    - train a logistic regression model
    - predict churn probability (0: didn't churn 1: did churn). 
        - for the `predict_proba result`, we are interested in the `did churn` result
    - compare ML prediction vs rule-based risk

- Once we calculate the churn probability, we must add it to the database. Functions for this in `ml.py`
- Next step is to add the `ml_churn_probability` in the API and frontend
- We then create `update_ml_churn.py` that stays in the `analytics/management/commands/` to update the ml churns outside of the app maybe through a cron job.
- We shall update the app from the file `update_analytics.sh` which has the customer health and ml churn files 
- Next is to modifty the train churn model so that we include evaluation i.e. `train-test-split` and calculate `accuracy`.








    
    