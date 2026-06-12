# Smart Hospital Management System

A database systems project for designing and implementing a Smart Hospital Management System. The repository contains the Phase 1 EERD deliverables and the Phase 2 MySQL-backed Flask application that demonstrates the database schema through a working CRUD web interface, reports, and reusable SQL views.

## Project Overview

The system models core hospital operations such as patient registration, staff management, doctor and nurse specialization, appointment scheduling, room admissions, billing, payments, medical records, and prescriptions. The implementation focuses on translating the EERD into a relational MySQL schema with primary keys, foreign keys, weak entities, specialization constraints, relationship tables, sample data, triggers, and reporting views.

## Phases

### Phase 1: Database Design

Phase 1 includes the conceptual database design artifacts:

- EERD documentation in Word format.
- Draw.io EERD diagram for the Smart Hospital Management System.

### Phase 2: Database Implementation

Phase 2 includes a complete MySQL and Flask implementation:

- MySQL schema script with tables, constraints, triggers, sample data, views, and advanced queries.
- Flask web application connected to MySQL.
- Generic CRUD screens for all configured entities.
- Dashboard with live database counts.
- Reports page using SQL views, joins, grouping, aggregation, and sorting.
- Schema mapping notes explaining how EERD relationships were implemented.

## Tech Stack

- Python
- Flask
- MySQL / MariaDB
- mysql-connector-python
- HTML, CSS, JavaScript
- Bootstrap
- XAMPP / phpMyAdmin for local database setup

## Repository Structure

```text
.
├── Phase 1/
│   ├── Smart Hospital Management.drawio
│   └── Smart_Hospital_Management_EERD.docx
├── Phase 2/
│   └── smart_hospital_phase2/
│       ├── main.py
│       ├── config.py
│       ├── db_connection.py
│       ├── requirements.txt
│       ├── SCHEMA_MAPPING.md
│       ├── models/
│       ├── sql/
│       ├── static/
│       └── templates/
├── .gitignore
└── README.md
```

## Database Highlights

The Phase 2 schema implements:

- Strong entities: Patient, Staff, Department, Room, Appointment, Bill, Payment.
- Specialization: Doctor, Nurse, and Admin as Staff subtypes.
- Weak entities: MedicalRecord and Prescription with composite primary keys.
- Many-to-many relationship: PatientRoom for patient room admissions.
- One-to-one relationship: Bill and Payment through a unique BillID in Payment.
- Integrity constraints using primary keys, foreign keys, unique constraints, checks, and triggers.
- SQL views for appointment schedules, doctor workload, revenue by department, room admissions, bill status, and patient medical history.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NawabIkram/Smart-Hospital-Management-System.git
cd Smart-Hospital-Management-System
```

### 2. Set Up the Database

Start Apache and MySQL from XAMPP, then import:

```text
Phase 2/smart_hospital_phase2/sql/hospital_schema.sql
```

You can import the script from phpMyAdmin, or run it with the MySQL command line:

```bash
mysql -u root < "Phase 2/smart_hospital_phase2/sql/hospital_schema.sql"
```

The script creates and uses the database:

```text
smart_hospital_db
```

### 3. Install Python Dependencies

```bash
cd "Phase 2/smart_hospital_phase2"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Database Connection

The default configuration is designed for local XAMPP:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=smart_hospital_db
DB_PORT=3306
```

These values can be overridden with environment variables if your MySQL setup is different.

### 5. Run the Application

```bash
python main.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Key Application Modules

- `main.py`: Flask routes for dashboard, CRUD pages, reports, database views, and error handling.
- `config.py`: Database configuration with environment variable support.
- `db_connection.py`: MySQL connection and query helper functions.
- `models/entity_config.py`: Whitelisted table and field configuration for generic CRUD pages.
- `models/crud.py`: Shared create, read, update, delete, search, and validation logic.
- `models/reports.py`: Advanced report queries using reusable SQL views.
- `models/db_views.py`: Database view metadata and display queries.
- `sql/hospital_schema.sql`: Complete database creation, sample data, views, and advanced SQL examples.

## Reports and Views

The application demonstrates advanced SQL concepts through:

- Appointment schedule with patient and doctor details.
- Doctor workload summary.
- Revenue by department.
- Room admission history.
- Bill status summary.
- Patient medical history view.

## Academic Purpose

This project was built as a database course assignment to demonstrate the full flow from conceptual EERD design to relational schema implementation and a connected application interface.
