"""
Reusable MySQL database views for the Views page.
Each item points to a CREATE VIEW statement from sql/hospital_schema.sql.
"""

from db_connection import execute_select


DATABASE_VIEWS = {
    "vw_appointment_schedule": {
        "title": "Appointment Schedule View",
        "purpose": "Shows appointments with patient name, doctor name, specialization, date, time, and status.",
        "query": "SELECT * FROM vw_appointment_schedule ORDER BY Date DESC, Time DESC",
    },
    "vw_doctor_workload": {
        "title": "Doctor Workload View",
        "purpose": "Shows each doctor with department, specialization, and total appointments.",
        "query": "SELECT * FROM vw_doctor_workload ORDER BY TotalAppointments DESC, DoctorName ASC",
    },
    "vw_revenue_by_department": {
        "title": "Revenue by Department View",
        "purpose": "Shows total bills, total revenue, and average bill amount department-wise.",
        "query": "SELECT * FROM vw_revenue_by_department ORDER BY TotalRevenue DESC",
    },
    "vw_room_admissions": {
        "title": "Room Admissions View",
        "purpose": "Shows admitted patients with room type, charges, admission date, and discharge date.",
        "query": "SELECT * FROM vw_room_admissions ORDER BY AdmissionDate DESC",
    },
    "vw_bill_status_summary": {
        "title": "Bill Status Summary View",
        "purpose": "Shows bill count and amount summary grouped by Paid, Unpaid, and Partial status.",
        "query": "SELECT * FROM vw_bill_status_summary ORDER BY TotalAmount DESC",
    },
    "vw_patient_medical_history": {
        "title": "Patient Medical History View",
        "purpose": "Shows patient basic details with diagnosis, treatment, and medical record date.",
        "query": "SELECT * FROM vw_patient_medical_history ORDER BY RecordDate DESC, PatientName ASC",
    },
}


def load_database_views():
    view_data = []
    for view_name, view_info in DATABASE_VIEWS.items():
        rows = execute_select(view_info["query"])
        view_data.append({
            "name": view_name,
            "title": view_info["title"],
            "purpose": view_info["purpose"],
            "query": view_info["query"],
            "columns": list(rows[0].keys()) if rows else [],
            "rows": rows,
        })
    return view_data
