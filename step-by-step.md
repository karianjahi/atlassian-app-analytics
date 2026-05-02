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






    