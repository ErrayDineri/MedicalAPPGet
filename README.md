# Medical Radiology Management System

A comprehensive Django-based web application for managing medical radiology workflows, patient records, and staff administration in healthcare facilities.

## 🏥 Features

### Role-Based Access Control
- **Administrator**: Complete system management with personnel oversight
- **Radiologist (Médecin)**: Report review, validation, and patient history access
- **Technician (Technicien)**: Patient registration and medical imaging upload

### Core Functionality
- **Patient Management**: Registration, search, and medical record maintenance
- **Medical Imaging**: Secure upload and storage of radiology scans
- **Report Workflow**: Structured reporting from imaging to validation
- **Personnel Administration**: Staff management with archive/reactivate capabilities
- **Secure Authentication**: Role-based login with archived user protection


## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (recommended)
- Git (for version control)
- A modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ErrayDineri/MedicalAPPGet
   cd MedicalAPPGet
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (Administrator)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:8000`

## 📦 Dependencies

The application requires the following Python packages:

```
asgiref==3.9.1
Django==5.2.4
pillow==11.3.0
sqlparse==0.5.3
tzdata==2025.2
```

Create a `requirements.txt` file with these dependencies for easy installation.

## 🏗️ Project Structure

```
MedicalAPPGet/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database (created after migration)
├── medical/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Application settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── main/                    # Main application
│   ├── __init__.py
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # Application configuration
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL patterns
│   ├── migrations/         # Database migrations
│   └── templates/          # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
└── MedicalUML/             # Project documentation
    ├── Classe.jpg
    ├── Diagram.mdj
    └── html-docs/
```

## 🗄️ Database Models

### User Model
- Custom user model with role-based permissions
- Roles: `admin`, `medecin`, `technicien`
- Archive functionality for staff management

### Patient Model
- Comprehensive patient information
- Unique reference dossier system
- Audit trail with creation timestamps

### Report Model
- Medical imaging storage
- Validation workflow
- Audit trail with technician and radiologist tracking

## 👥 User Roles & Workflows

### Administrator Dashboard
- **Personnel Management**: Add, archive, and reactivate staff
- **Statistics Overview**: Active users, doctors, technicians
- **Password Management**: Reset user passwords with secure generation
- **System Oversight**: Complete access to all system functions

### Radiologist (Médecin) Dashboard
- **Report Review**: Access to pending and validated reports
- **Report Validation**: Approve medical reports after review
- **Patient History**: Complete medical imaging history per patient
- **Report Editing**: Modify report content before validation

### Technician (Technicien) Dashboard
- **Patient Search**: Find existing patients by reference dossier
- **Patient Registration**: Add new patients to the system
- **Image Upload**: Attach medical scans to patient records
- **Workflow Tracking**: View recent uploads and reports

## 🔐 Security Features

- **Role-based Access Control**: Each user type has specific permissions
- **Archived User Protection**: Prevents login for deactivated accounts
- **CSRF Protection**: Prevents cross-site request forgery attacks
- **Secure Password Handling**: Django's built-in password hashing
- **Session Management**: Secure session handling with timeout

## 📱 User Interface

### Design Principles
- **Medical Professional**: Clean, professional appearance suitable for healthcare
- **Accessibility**: High contrast colors and readable typography
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Intuitive**: Clear navigation and workflow-based design

### Color Scheme
- **Primary Color**: #303990 (Professional blue)
- **Secondary Color**: #fbba21 (Accent gold)
- **Semantic Colors**: Success, warning, and error states
- **Neutral Grays**: For backgrounds and text

## 📝 To-Do

- **Email**: Password set-up by employee through a temporary link. Same for reset.
- **Interactive Report**: Upgrade the UX to allow better interactivity with the report, the image etc...
- **Celery and AI**: Reports automatically generated with AI.