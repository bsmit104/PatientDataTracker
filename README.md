# PatientDataTracker

A robust, Django-based web application for managing patient records, deployed on Render with PostgreSQL. Features interactive Chart.js visualizations, real-time search, staff authentication, and data export capabilities—built to showcase full-stack development skills with a focus on usability and scalability.

## Demo Video

[![PatientDataTracker Demo](https://img.youtube.com/vi/xgoSJBTjM2s/0.jpg)](https://youtu.be/XxfaHredDv4)

*Click the thumbnail above to watch a demo of the app in action!*

## Live Deployment

Explore the app live at: [https://patientdatatracker.onrender.com/](https://patientdatatracker.onrender.com/)

*Staff Login: Username: `test`, Password: `testpassword` (demo purposes only)*

## Features

- **Patient Management**: Add, edit, delete, and view detailed patient records (name, age, recent diagnosis, allergens, past diagnoses, notes) with staff-only access.
- **Interactive Charts**: Visualize data with Chart.js—bar (age groups), pie (top diagnoses), line (registrations over time), and heatmap (diagnoses by age), switchable via dropdown.
- **Real-Time Insights**: Sidebar with recently viewed patients (top 5) and recent actions (last 7: add/edit/delete/view logs).
- **Search Functionality**: Filter patients by name, recent diagnosis, treatment, age, or diagnosis date.
- **Data Export**: Download patient records as CSV (staff-only).
- **Edit History**: Track changes to patient records with user and timestamp logs (last 5 per patient).
- **Dashboard Widgets**: Quick stats on patient list—total patients, average age, top diagnosis.
- **Responsive Design**: Bootstrap-powered UI with dark/light mode toggle for accessibility.
- **Mock Data**: 60 dynamically generated patients using Faker for testing and demo purposes.

## Tech Stack

- **Backend**: Django, PostgreSQL, WhiteNoise (static file serving)
- **Frontend**: Bootstrap 5, Chart.js, HTML/CSS/JavaScript
- **Deployment**: Render (PaaS), GitHub for version control
- **Tools**: Python, Gunicorn, Faker, Django Authentication

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Git

### Local Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bsmit104/PatientDataTracker.git
   cd PatientDataTracker

**Set Up Virtual Environment**:
   python -m venv venv
   venv\Scripts\activate  # Windows

   source venv/bin/activate  # Mac/Linux

**Install Dependencies**:
   pip install -r requirements.txt

**Configure PostgreSQL**:
   Create a database named patient_tracker in PostgreSQL (e.g., via pgAdmin).
   Update settings.py with your local DB credentials if needed (default: test/testpassword/localhost:5432).

**Run Migrations & Load Mock Data**:
   python manage.py migrate
   python manage.py createsuperuser  # Create admin user (e.g., test/testpassword)
   python manage.py load_mock_data  # Generate 60 sample patients
   Start the Server:

   python manage.py runserver 0.0.0.0:8001
   Visit http://127.0.0.1:8001/ in your browser.

## Deployment
Deployed on Render with a free PostgreSQL instance and Gunicorn.
Build Command: pip install -r requirements.txt && python manage.py migrate && python manage.py create_superuser && python manage.py load_mock_data && python manage.py collectstatic --noinput
See Render logs for deployment details.
Project Highlights
## Scalability: 
Modular Django structure, ready for additional features or API integration.
## User Experience: 
Responsive UI with dark/light modes, interactive charts, and real-time feedback enhance usability.
Data Integrity: Edit history and action logs ensure traceability, critical for medical applications.
## Automation: 
Faker-generated mock data and CSV export streamline testing and reporting.
Future Enhancements
REST API with Django REST Framework for third-party integration.
Role-based access control (e.g., admin vs. staff permissions).
Real-time search with AJAX for instant filtering.
Notifications for staff actions (e.g., "Patient added" alerts).
### Contact
Built by Brayden Smith. Reach out at jbrayden35@gmail.com or LinkedIn https://www.linkedin.com/in/braydenjsmith22/ for questions or collaboration!
