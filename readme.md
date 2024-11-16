# Event Management System

Welcome to the **Event Management System**, a Django-based project designed to manage events, attendees, reservations, and related roles. This project includes an admin portal for advanced management and a REST API for seamless integration with other systems.

---

## Project Features

- **Admin Portal**: Manage users, roles, events, reservations, and speakers with advanced filtering and actions.
- **REST API**: Endpoints to handle operations for events, reservations, attendees, and authentication.
- **Role-based Permissions**: Control access to specific actions based on roles and permissions.
- **Scalable Design**: Built with best practices for scalability and maintainability.
- **Postman Collection**: Ready-to-use Postman collection to test endpoints.

---

## Installation Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository

git clone <repository-url> cd <project-folder>

### 2. Set Up a Virtual Environment

conda create -n env python=3.10 # activate env

### 3. Install Dependencies
Install the required Python libraries using `pip`:
on requirements folder :
* pip install -r requirements.txt

### 4. Configure Environment Variables
Rename the file .example_env to .env and provide the necesary environment variables

### 5. Apply Database Migrations
Run migrations to set up the database schema:
python manage.py makemigrations python manage.py migrate

### 6. Seed Initial Data
After applying the database migrations, you can populate the database with initial data by running the custom seed script located at `src/core/management/commands/seed_data.py`.

This script sets up basic data such as roles, categories, and other initial configurations required for the project to function properly.

#### Run the Seed Script
Execute the following command:
python manage.py seed_data

#### What Does the Seed Script Do?
- Creates default **roles** (e.g., Admin, Event Manager).
- Populates **categories** for events.
- Adds any other pre-defined configurations needed for the system.

You can review or customize the seed data by editing the `seed_data.py` file.

### 7. Create a Superuser
To access the admin portal, create a superuser:
python manage.py createsuperuser
Follow the prompts to set up the username, email, and password.

### 8. Run the Development Server
Start the Django development server:
python manage.py runserver

Visit `http://localhost:8000/v1/api/admin/` to access the admin portal.
Once you are inside the Admin portal, you will be able to manage roles, permissions (full crud on events and reservations), users and more.

### 9. Docs
The OpenAPI docs are located here: `http://localhost:8000/docs/`
Remember to run the login and copy the token, then click Authorize at the top right and add the word Bearer <token>
However, the postman collection is available in the repo so you can import it.

### 10. Database diagram
The ER diagram is available in the repo, it is the file `db_diagram_viamericas.png` .

### 11. Reports
To generate the reports in .xlsx use the endpoint located in the Report folder within Event, in the postman collection.

### Contact
If you encounter issues or have questions, please reach out to the project maintainer at hasalara96@gmail.com