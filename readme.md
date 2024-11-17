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

### PROJECT DEPLOY:
To access the online service, you can do so through this link:
`https://eventmanagement-production-92c0.up.railway.app/docs/`
The backend is hosted there.
Note that this service already has data in the db provided by the seed_data file that you will find later.
Use the credentials that were sent to the email with this repo to access the admin portal.
`https://eventmanagement-production-92c0.up.railway.app/v1/api/admin/`

## Installation Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository

git clone https://github.com/hasala1996/event_management cd "project-folder"

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
- python manage.py makemigrations
- python manage.py migrate

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
- python manage.py createsuperuser
- Follow the prompts to set up the username, email, and password.

### 8. Run the Development Server
Start the Django development server:
- python manage.py runserver

Visit `http://localhost:8000/v1/api/admin/` to access the admin portal.
Once you are inside the Admin portal, you will be able to manage roles, permissions (full crud on events and reservations), users and more.

### 9. Running the Project with Docker:
To simplify the setup and ensure consistency across development environments, you can run the project using Docker and Docker Compose.

## Prerequisites
- Docker: Make sure Docker is installed on your machine. You can download it from Docker Desktop.
- Docker Compose: Usually included with Docker Desktop. Verify it's installed by running docker-compose --version in your terminal.
### Build and Run the Containers
Being in the src folder of the project, execute:

- docker-compose up --build

This command will:

- Build the Docker image for your Django application.
- Start the services defined in docker-compose.yml, which include the backend (Django) and the PostgreSQL database.
- Apply migrations and start the development server.


### 10. Docs
- The OpenAPI docs are located here: `http://localhost:8000/docs/`
- Remember to run the login and copy the token, then click Authorize at the top right and add the word Bearer <token>
- However, the postman collection is available in the repo so you can import it.

### 11. Database diagram
The ER diagram is available in the repo, it is the file `db_diagram_viamericas.png` .

### 12. Reports
To generate the reports in .xlsx use the endpoint located in the Report folder within Event, in the postman collection.

### 13. Coverage
To execute the test coverage commands while located in the `src` directory of the project, follow these steps:
- Navigate to the src Directory
- Open your terminal or command prompt and change to the src directory of your project , and execute:
`coverage run -m pytest --ds=config.settings.settings_test`
After the tests have been executed, generate a coverage report with:
`coverage report -m`
This report provides a summary of the code coverage.

### Contact
If you encounter issues or have questions, please reach out to the project maintainer at hasalara96@gmail.com