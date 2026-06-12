"""
Entity configuration for generic CRUD pages.

Important:
- Only tables/columns listed here are allowed in dynamic SQL.
- This keeps the generic CRUD code safe from SQL injection in identifiers.
"""

ENTITIES = {
    "patients": {
        "display_name": "Patients",
        "table": "Patient",
        "pk": ["PatientID"],
        "search_fields": ["FirstName", "LastName", "Phone", "Gender"],
        "fields": [
            {"name": "PatientID", "label": "Patient ID", "type": "number", "auto": True},
            {"name": "FirstName", "label": "First Name", "type": "text", "required": True},
            {"name": "LastName", "label": "Last Name", "type": "text", "required": True},
            {"name": "DOB", "label": "Date of Birth", "type": "date", "required": True},
            {"name": "Age", "label": "Age", "type": "number", "required": True, "min": 0},
            {"name": "Gender", "label": "Gender", "type": "select", "required": True,
             "options": ["Male", "Female", "Other"]},
            {"name": "Phone", "label": "Phone", "type": "text", "required": True},
            {"name": "Address", "label": "Address", "type": "textarea", "required": True},
        ],
    },

    "departments": {
        "display_name": "Departments",
        "table": "Department",
        "pk": ["DeptID"],
        "search_fields": ["DeptName", "Location"],
        "fields": [
            {"name": "DeptID", "label": "Department ID", "type": "number", "auto": True},
            {"name": "DeptName", "label": "Department Name", "type": "text", "required": True},
            {"name": "Location", "label": "Location", "type": "text", "required": True},
        ],
    },

    "staff": {
        "display_name": "Staff",
        "table": "Staff",
        "pk": ["StaffID"],
        "search_fields": ["FirstName", "LastName", "Phone", "StaffType"],
        "fields": [
            {"name": "StaffID", "label": "Staff ID", "type": "number", "auto": True},
            {"name": "FirstName", "label": "First Name", "type": "text", "required": True},
            {"name": "LastName", "label": "Last Name", "type": "text", "required": True},
            {"name": "Salary", "label": "Salary", "type": "number", "required": True, "min": 0, "step": "0.01"},
            {"name": "Phone", "label": "Phone", "type": "text", "required": True},
            {"name": "StaffType", "label": "Staff Type", "type": "select", "required": True,
             "options": ["Doctor", "Nurse", "Admin"]},
        ],
    },

    "nurses": {
        "display_name": "Nurses",
        "table": "Nurse",
        "pk": ["NurseID"],
        "search_fields": ["Shift", "Qualification"],
        "fields": [
            {"name": "NurseID", "label": "Nurse Staff ID", "type": "select", "required": True,
             "options_query": "SELECT StaffID AS value, CONCAT(StaffID, ' - ', FirstName, ' ', LastName) AS label FROM Staff WHERE StaffType='Nurse' ORDER BY StaffID"},
            {"name": "Shift", "label": "Shift", "type": "select", "required": True,
             "options": ["Morning", "Evening", "Night"]},
            {"name": "Qualification", "label": "Qualification", "type": "text", "required": True},
        ],
    },

    "doctors": {
        "display_name": "Doctors",
        "table": "Doctor",
        "pk": ["DoctorID"],
        "search_fields": ["Specialization"],
        "fields": [
            {"name": "DoctorID", "label": "Doctor Staff ID", "type": "select", "required": True,
             "options_query": "SELECT StaffID AS value, CONCAT(StaffID, ' - ', FirstName, ' ', LastName) AS label FROM Staff WHERE StaffType='Doctor' ORDER BY StaffID"},
            {"name": "Specialization", "label": "Specialization", "type": "text", "required": True},
            {"name": "ExperienceYears", "label": "Experience Years", "type": "number", "required": True, "min": 0},
            {"name": "DeptID", "label": "Department", "type": "select", "required": True,
             "options_query": "SELECT DeptID AS value, CONCAT(DeptID, ' - ', DeptName) AS label FROM Department ORDER BY DeptName"},
            {"name": "NurseID", "label": "Assisting Nurse", "type": "select", "required": False,
             "options_query": "SELECT NurseID AS value, CONCAT(NurseID, ' - ', s.FirstName, ' ', s.LastName) AS label FROM Nurse n JOIN Staff s ON s.StaffID=n.NurseID ORDER BY s.FirstName"},
        ],
    },

    "admins": {
        "display_name": "Admins",
        "table": "Admin",
        "pk": ["AdminID"],
        "search_fields": ["Role"],
        "fields": [
            {"name": "AdminID", "label": "Admin Staff ID", "type": "select", "required": True,
             "options_query": "SELECT StaffID AS value, CONCAT(StaffID, ' - ', FirstName, ' ', LastName) AS label FROM Staff WHERE StaffType='Admin' ORDER BY StaffID"},
            {"name": "Role", "label": "Role", "type": "text", "required": True},
        ],
    },

    "rooms": {
        "display_name": "Rooms",
        "table": "Room",
        "pk": ["RoomID"],
        "search_fields": ["RoomType"],
        "fields": [
            {"name": "RoomID", "label": "Room ID", "type": "number", "auto": True},
            {"name": "RoomType", "label": "Room Type", "type": "text", "required": True},
            {"name": "Charges", "label": "Charges", "type": "number", "required": True, "min": 0, "step": "0.01"},
        ],
    },

    "patient_rooms": {
        "display_name": "Patient Room Admissions",
        "table": "PatientRoom",
        "pk": ["PatientID", "RoomID", "AdmissionDate"],
        "search_fields": [],
        "fields": [
            {"name": "PatientID", "label": "Patient", "type": "select", "required": True,
             "options_query": "SELECT PatientID AS value, CONCAT(PatientID, ' - ', FirstName, ' ', LastName) AS label FROM Patient ORDER BY FirstName"},
            {"name": "RoomID", "label": "Room", "type": "select", "required": True,
             "options_query": "SELECT RoomID AS value, CONCAT(RoomID, ' - ', RoomType) AS label FROM Room ORDER BY RoomID"},
            {"name": "AdmissionDate", "label": "Admission Date", "type": "date", "required": True},
            {"name": "DischargeDate", "label": "Discharge Date", "type": "date", "required": False},
        ],
    },

    "appointments": {
        "display_name": "Appointments",
        "table": "Appointment",
        "pk": ["AppointmentID"],
        "search_fields": ["Status"],
        "fields": [
            {"name": "AppointmentID", "label": "Appointment ID", "type": "number", "auto": True},
            {"name": "PatientID", "label": "Patient", "type": "select", "required": True,
             "options_query": "SELECT PatientID AS value, CONCAT(PatientID, ' - ', FirstName, ' ', LastName) AS label FROM Patient ORDER BY FirstName"},
            {"name": "DoctorID", "label": "Doctor", "type": "select", "required": True,
             "options_query": "SELECT DoctorID AS value, CONCAT(DoctorID, ' - Dr. ', s.FirstName, ' ', s.LastName, ' (', d.Specialization, ')') AS label FROM Doctor d JOIN Staff s ON s.StaffID=d.DoctorID ORDER BY s.FirstName"},
            {"name": "AdminID", "label": "Scheduled By Admin", "type": "select", "required": True,
             "options_query": "SELECT AdminID AS value, CONCAT(AdminID, ' - ', s.FirstName, ' ', s.LastName) AS label FROM Admin a JOIN Staff s ON s.StaffID=a.AdminID ORDER BY s.FirstName"},
            {"name": "Date", "label": "Appointment Date", "type": "date", "required": True},
            {"name": "Time", "label": "Appointment Time", "type": "time", "required": True},
            {"name": "Status", "label": "Status", "type": "select", "required": True,
             "options": ["Scheduled", "Completed", "Cancelled"]},
        ],
    },

    "bills": {
        "display_name": "Bills",
        "table": "Bill",
        "pk": ["BillID"],
        "search_fields": ["Status"],
        "fields": [
            {"name": "BillID", "label": "Bill ID", "type": "number", "auto": True},
            {"name": "AppointmentID", "label": "Appointment", "type": "select", "required": True,
             "options_query": "SELECT AppointmentID AS value, CONCAT(AppointmentID, ' - ', Date, ' ', Time) AS label FROM Appointment ORDER BY AppointmentID"},
            {"name": "Amount", "label": "Amount", "type": "number", "required": True, "min": 0, "step": "0.01"},
            {"name": "Date", "label": "Bill Date", "type": "date", "required": True},
            {"name": "Status", "label": "Status", "type": "select", "required": True,
             "options": ["Unpaid", "Paid", "Partial"]},
        ],
    },

    "payments": {
        "display_name": "Payments",
        "table": "Payment",
        "pk": ["PaymentID"],
        "search_fields": ["Method"],
        "fields": [
            {"name": "PaymentID", "label": "Payment ID", "type": "number", "auto": True},
            {"name": "BillID", "label": "Bill", "type": "select", "required": True,
             "options_query": "SELECT BillID AS value, CONCAT(BillID, ' - Amount: ', Amount, ' - ', Status) AS label FROM Bill ORDER BY BillID"},
            {"name": "Method", "label": "Payment Method", "type": "select", "required": True,
             "options": ["Cash", "Card", "Bank Transfer", "Insurance"]},
            {"name": "PaymentDate", "label": "Payment Date", "type": "date", "required": True},
        ],
    },

    "medical_records": {
        "display_name": "Medical Records",
        "table": "MedicalRecord",
        "pk": ["PatientID", "RecordID"],
        "search_fields": ["Diagnosis", "Treatment"],
        "fields": [
            {"name": "PatientID", "label": "Patient", "type": "select", "required": True,
             "options_query": "SELECT PatientID AS value, CONCAT(PatientID, ' - ', FirstName, ' ', LastName) AS label FROM Patient ORDER BY FirstName"},
            {"name": "RecordID", "label": "Record ID", "type": "number", "required": True, "min": 1},
            {"name": "Diagnosis", "label": "Diagnosis", "type": "text", "required": True},
            {"name": "Treatment", "label": "Treatment", "type": "textarea", "required": True},
            {"name": "Date", "label": "Record Date", "type": "date", "required": True},
        ],
    },

    "prescriptions": {
        "display_name": "Prescriptions",
        "table": "Prescription",
        "pk": ["AppointmentID", "PrescriptionID"],
        "search_fields": ["Medicines", "Dosage"],
        "fields": [
            {"name": "AppointmentID", "label": "Appointment", "type": "select", "required": True,
             "options_query": "SELECT AppointmentID AS value, CONCAT(AppointmentID, ' - ', Date, ' ', Time) AS label FROM Appointment ORDER BY AppointmentID"},
            {"name": "PrescriptionID", "label": "Prescription ID", "type": "number", "required": True, "min": 1},
            {"name": "Medicines", "label": "Medicines", "type": "textarea", "required": True},
            {"name": "Dosage", "label": "Dosage", "type": "text", "required": True},
            {"name": "Date", "label": "Prescription Date", "type": "date", "required": True},
        ],
    },
}


def get_entity(entity_key):
    return ENTITIES.get(entity_key)


def get_navigation_entities():
    return ENTITIES
