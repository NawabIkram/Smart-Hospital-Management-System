"""
Advanced SQL queries for the Reports page.

These demonstrate reusable MySQL VIEWS plus JOIN, GROUP BY, ORDER BY, COUNT, SUM, and AVG.
"""

from db_connection import execute_select


def appointment_schedule():
    query = """
        SELECT * FROM vw_appointment_schedule
        ORDER BY Date DESC, Time DESC
    """
    return execute_select(query)


def doctor_workload():
    query = """
        SELECT * FROM vw_doctor_workload
        ORDER BY TotalAppointments DESC, DoctorName ASC
    """
    return execute_select(query)


def revenue_by_department():
    query = """
        SELECT * FROM vw_revenue_by_department
        ORDER BY TotalRevenue DESC
    """
    return execute_select(query)


def room_admissions():
    query = """
        SELECT * FROM vw_room_admissions
        ORDER BY AdmissionDate DESC
    """
    return execute_select(query)


def bill_status_summary():
    query = """
        SELECT * FROM vw_bill_status_summary
        ORDER BY TotalAmount DESC
    """
    return execute_select(query)


def dashboard_counts():
    query = """
        SELECT 'Patients' AS Label, COUNT(*) AS Total FROM Patient
        UNION ALL SELECT 'Staff', COUNT(*) FROM Staff
        UNION ALL SELECT 'Appointments', COUNT(*) FROM Appointment
        UNION ALL SELECT 'Bills', COUNT(*) FROM Bill
        UNION ALL SELECT 'Rooms', COUNT(*) FROM Room
        UNION ALL SELECT 'Payments', COUNT(*) FROM Payment
    """
    return execute_select(query)


REPORTS = {
    "appointment_schedule": {
        "title": "Appointment Schedule with Patient and Doctor",
        "description": "VIEW + JOIN + ORDER BY",
        "function": appointment_schedule,
    },
    "doctor_workload": {
        "title": "Doctor Workload",
        "description": "VIEW + GROUP BY + COUNT + ORDER BY",
        "function": doctor_workload,
    },
    "revenue_by_department": {
        "title": "Revenue by Department",
        "description": "VIEW + GROUP BY + SUM + AVG + ORDER BY",
        "function": revenue_by_department,
    },
    "room_admissions": {
        "title": "Room Admission History",
        "description": "VIEW + JOIN + ORDER BY",
        "function": room_admissions,
    },
    "bill_status_summary": {
        "title": "Bill Status Summary",
        "description": "VIEW + GROUP BY + COUNT + SUM + AVG",
        "function": bill_status_summary,
    },
}
