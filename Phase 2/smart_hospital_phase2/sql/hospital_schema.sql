-- Smart Hospital Management System
-- Database Systems Phase 2
-- MySQL / MariaDB script for XAMPP phpMyAdmin

DROP DATABASE IF EXISTS smart_hospital_db;
CREATE DATABASE smart_hospital_db;
USE smart_hospital_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Bill;
DROP TABLE IF EXISTS Prescription;
DROP TABLE IF EXISTS MedicalRecord;
DROP TABLE IF EXISTS PatientRoom;
DROP TABLE IF EXISTS Appointment;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Doctor;
DROP TABLE IF EXISTS Nurse;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Staff;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================
-- STRONG ENTITIES
-- =========================

CREATE TABLE Patient (
    PatientID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    Age INT NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE,
    Address VARCHAR(255) NOT NULL,
    CHECK (Age >= 0)
) ENGINE=InnoDB;

CREATE TABLE Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE,
    StaffType ENUM('Doctor', 'Nurse', 'Admin') NOT NULL,
    CHECK (Salary >= 0)
) ENGINE=InnoDB;

CREATE TABLE Department (
    DeptID INT AUTO_INCREMENT PRIMARY KEY,
    DeptName VARCHAR(100) NOT NULL UNIQUE,
    Location VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Nurse (
    NurseID INT PRIMARY KEY,
    Shift ENUM('Morning', 'Evening', 'Night') NOT NULL,
    Qualification VARCHAR(100) NOT NULL,
    CONSTRAINT fk_nurse_staff
        FOREIGN KEY (NurseID) REFERENCES Staff(StaffID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    Role VARCHAR(100) NOT NULL,
    CONSTRAINT fk_admin_staff
        FOREIGN KEY (AdminID) REFERENCES Staff(StaffID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    Specialization VARCHAR(100) NOT NULL,
    ExperienceYears INT NOT NULL,
    DeptID INT NOT NULL,
    NurseID INT NULL,
    CHECK (ExperienceYears >= 0),
    CONSTRAINT fk_doctor_staff
        FOREIGN KEY (DoctorID) REFERENCES Staff(StaffID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_doctor_department
        FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_doctor_nurse
        FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE Room (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    RoomType VARCHAR(50) NOT NULL,
    Charges DECIMAL(10,2) NOT NULL,
    CHECK (Charges >= 0)
) ENGINE=InnoDB;

-- M:N relationship between Patient and Room: AdmittedTo
CREATE TABLE PatientRoom (
    PatientID INT NOT NULL,
    RoomID INT NOT NULL,
    AdmissionDate DATE NOT NULL,
    DischargeDate DATE NULL,
    PRIMARY KEY (PatientID, RoomID, AdmissionDate),
    CONSTRAINT fk_patientroom_patient
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_patientroom_room
        FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CHECK (DischargeDate IS NULL OR DischargeDate >= AdmissionDate)
) ENGINE=InnoDB;

CREATE TABLE Appointment (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AdminID INT NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Status ENUM('Scheduled', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Scheduled',
    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_appointment_admin
        FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_doctor_datetime UNIQUE (DoctorID, Date, Time)
) ENGINE=InnoDB;

-- Pays relationship represented through Bill linked to Appointment.
CREATE TABLE Bill (
    BillID INT AUTO_INCREMENT PRIMARY KEY,
    AppointmentID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Date DATE NOT NULL,
    Status ENUM('Unpaid', 'Paid', 'Partial') NOT NULL DEFAULT 'Unpaid',
    CHECK (Amount >= 0),
    CONSTRAINT fk_bill_appointment
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- 1:1 relationship between Bill and Payment. Payment participation is total.
CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    BillID INT NOT NULL UNIQUE,
    Method ENUM('Cash', 'Card', 'Bank Transfer', 'Insurance') NOT NULL,
    PaymentDate DATE NOT NULL,
    CONSTRAINT fk_payment_bill
        FOREIGN KEY (BillID) REFERENCES Bill(BillID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- Weak entity identified by Patient.
CREATE TABLE MedicalRecord (
    PatientID INT NOT NULL,
    RecordID INT NOT NULL,
    Diagnosis VARCHAR(255) NOT NULL,
    Treatment TEXT NOT NULL,
    Date DATE NOT NULL,
    PRIMARY KEY (PatientID, RecordID),
    CONSTRAINT fk_medicalrecord_patient
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- Weak entity identified by Appointment.
CREATE TABLE Prescription (
    AppointmentID INT NOT NULL,
    PrescriptionID INT NOT NULL,
    Medicines TEXT NOT NULL,
    Dosage VARCHAR(255) NOT NULL,
    Date DATE NOT NULL,
    PRIMARY KEY (AppointmentID, PrescriptionID),
    CONSTRAINT fk_prescription_appointment
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- =========================
-- ISA TYPE VALIDATION TRIGGERS
-- =========================
-- These triggers enforce the disjoint/total specialization:
-- a Staff row inserted into Doctor must have StaffType='Doctor', etc.

DELIMITER //

CREATE TRIGGER trg_doctor_staff_type_insert
BEFORE INSERT ON Doctor
FOR EACH ROW
BEGIN
    IF (SELECT StaffType FROM Staff WHERE StaffID = NEW.DoctorID) <> 'Doctor' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'DoctorID must reference a Staff row with StaffType = Doctor';
    END IF;
END//

CREATE TRIGGER trg_nurse_staff_type_insert
BEFORE INSERT ON Nurse
FOR EACH ROW
BEGIN
    IF (SELECT StaffType FROM Staff WHERE StaffID = NEW.NurseID) <> 'Nurse' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'NurseID must reference a Staff row with StaffType = Nurse';
    END IF;
END//

CREATE TRIGGER trg_admin_staff_type_insert
BEFORE INSERT ON Admin
FOR EACH ROW
BEGIN
    IF (SELECT StaffType FROM Staff WHERE StaffID = NEW.AdminID) <> 'Admin' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'AdminID must reference a Staff row with StaffType = Admin';
    END IF;
END//

DELIMITER ;

-- =========================
-- SAMPLE DATA
-- =========================

INSERT INTO Patient (PatientID, FirstName, LastName, DOB, Age, Gender, Phone, Address) VALUES
(1, 'Ali', 'Khan', '2001-05-12', 23, 'Male', '03001234567', 'Lahore'),
(2, 'Ayesha', 'Malik', '1998-09-20', 26, 'Female', '03017654321', 'Karachi'),
(3, 'Bilal', 'Ahmed', '1988-02-10', 36, 'Male', '03111234567', 'Islamabad'),
(4, 'Fatima', 'Noor', '1995-12-03', 29, 'Female', '03221234567', 'Multan');

INSERT INTO Department (DeptID, DeptName, Location) VALUES
(1, 'Cardiology', 'Block A'),
(2, 'Neurology', 'Block B'),
(3, 'Emergency', 'Ground Floor'),
(4, 'Pediatrics', 'Block C');

INSERT INTO Staff (StaffID, FirstName, LastName, Salary, Phone, StaffType) VALUES
(1, 'Ahmed', 'Raza', 150000.00, '03450000001', 'Doctor'),
(2, 'Sara', 'Iqbal', 170000.00, '03450000002', 'Doctor'),
(3, 'Hassan', 'Ali', 140000.00, '03450000003', 'Doctor'),
(4, 'Nimra', 'Shah', 85000.00, '03450000004', 'Nurse'),
(5, 'Zainab', 'Tariq', 90000.00, '03450000005', 'Nurse'),
(6, 'Usman', 'Farooq', 95000.00, '03450000006', 'Admin');

INSERT INTO Nurse (NurseID, Shift, Qualification) VALUES
(4, 'Morning', 'BS Nursing'),
(5, 'Night', 'Diploma Nursing');

INSERT INTO Admin (AdminID, Role) VALUES
(6, 'Appointment Manager');

INSERT INTO Doctor (DoctorID, Specialization, ExperienceYears, DeptID, NurseID) VALUES
(1, 'Cardiologist', 8, 1, 4),
(2, 'Neurologist', 10, 2, 5),
(3, 'Emergency Physician', 6, 3, 4);

INSERT INTO Room (RoomID, RoomType, Charges) VALUES
(1, 'General Ward', 3000.00),
(2, 'Private Room', 8000.00),
(3, 'ICU', 15000.00),
(4, 'Emergency Bed', 5000.00);

INSERT INTO PatientRoom (PatientID, RoomID, AdmissionDate, DischargeDate) VALUES
(1, 2, '2026-04-01', '2026-04-03'),
(2, 1, '2026-04-05', NULL),
(3, 3, '2026-04-06', '2026-04-10');

INSERT INTO Appointment (AppointmentID, PatientID, DoctorID, AdminID, Date, Time, Status) VALUES
(1, 1, 1, 6, '2026-04-15', '10:00:00', 'Completed'),
(2, 2, 2, 6, '2026-04-16', '11:30:00', 'Scheduled'),
(3, 3, 3, 6, '2026-04-17', '14:00:00', 'Completed'),
(4, 4, 1, 6, '2026-04-18', '09:00:00', 'Scheduled');

INSERT INTO Bill (BillID, AppointmentID, Amount, Date, Status) VALUES
(1, 1, 5000.00, '2026-04-15', 'Paid'),
(2, 2, 6500.00, '2026-04-16', 'Unpaid'),
(3, 3, 12000.00, '2026-04-17', 'Partial');

INSERT INTO Payment (PaymentID, BillID, Method, PaymentDate) VALUES
(1, 1, 'Cash', '2026-04-15');

INSERT INTO MedicalRecord (PatientID, RecordID, Diagnosis, Treatment, Date) VALUES
(1, 1, 'High Blood Pressure', 'Medication and weekly monitoring', '2026-04-15'),
(2, 1, 'Migraine', 'Pain relief medication and rest', '2026-04-16'),
(3, 1, 'Minor Injury', 'Wound cleaning and dressing', '2026-04-17');

INSERT INTO Prescription (AppointmentID, PrescriptionID, Medicines, Dosage, Date) VALUES
(1, 1, 'Amlodipine', '5mg once daily', '2026-04-15'),
(2, 1, 'Paracetamol, Ibuprofen', 'As prescribed after meals', '2026-04-16'),
(3, 1, 'Antibiotic Cream', 'Apply twice daily', '2026-04-17');


-- =========================
-- DATABASE VIEWS
-- =========================
-- Views are virtual tables made from SELECT queries.
-- They make complex JOIN/report queries easy to reuse in GUI and phpMyAdmin.

DROP VIEW IF EXISTS vw_appointment_schedule;
DROP VIEW IF EXISTS vw_doctor_workload;
DROP VIEW IF EXISTS vw_revenue_by_department;
DROP VIEW IF EXISTS vw_room_admissions;
DROP VIEW IF EXISTS vw_bill_status_summary;
DROP VIEW IF EXISTS vw_patient_medical_history;

CREATE VIEW vw_appointment_schedule AS
SELECT
    a.AppointmentID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    CONCAT('Dr. ', ds.FirstName, ' ', ds.LastName) AS DoctorName,
    d.Specialization,
    a.Date,
    a.Time,
    a.Status
FROM Appointment a
JOIN Patient p ON p.PatientID = a.PatientID
JOIN Doctor d ON d.DoctorID = a.DoctorID
JOIN Staff ds ON ds.StaffID = d.DoctorID;

CREATE VIEW vw_doctor_workload AS
SELECT
    d.DoctorID,
    CONCAT(s.FirstName, ' ', s.LastName) AS DoctorName,
    dept.DeptName,
    d.Specialization,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Doctor d
JOIN Staff s ON s.StaffID = d.DoctorID
JOIN Department dept ON dept.DeptID = d.DeptID
LEFT JOIN Appointment a ON a.DoctorID = d.DoctorID
GROUP BY d.DoctorID, DoctorName, dept.DeptName, d.Specialization;

CREATE VIEW vw_revenue_by_department AS
SELECT
    dept.DeptName,
    COUNT(b.BillID) AS TotalBills,
    SUM(b.Amount) AS TotalRevenue,
    AVG(b.Amount) AS AverageBill
FROM Bill b
JOIN Appointment a ON a.AppointmentID = b.AppointmentID
JOIN Doctor d ON d.DoctorID = a.DoctorID
JOIN Department dept ON dept.DeptID = d.DeptID
GROUP BY dept.DeptName;

CREATE VIEW vw_room_admissions AS
SELECT
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    r.RoomID,
    r.RoomType,
    r.Charges,
    pr.AdmissionDate,
    pr.DischargeDate
FROM PatientRoom pr
JOIN Patient p ON p.PatientID = pr.PatientID
JOIN Room r ON r.RoomID = pr.RoomID;

CREATE VIEW vw_bill_status_summary AS
SELECT
    Status,
    COUNT(*) AS NumberOfBills,
    SUM(Amount) AS TotalAmount,
    AVG(Amount) AS AverageAmount
FROM Bill
GROUP BY Status;

CREATE VIEW vw_patient_medical_history AS
SELECT
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    p.Gender,
    p.Phone,
    mr.RecordID,
    mr.Diagnosis,
    mr.Treatment,
    mr.Date AS RecordDate
FROM Patient p
JOIN MedicalRecord mr ON mr.PatientID = p.PatientID;


-- =========================
-- ADVANCED QUERY EXAMPLES
-- =========================

-- 1. Appointment schedule with patient and doctor names
SELECT
    a.AppointmentID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    CONCAT('Dr. ', ds.FirstName, ' ', ds.LastName) AS DoctorName,
    d.Specialization,
    a.Date,
    a.Time,
    a.Status
FROM Appointment a
JOIN Patient p ON p.PatientID = a.PatientID
JOIN Doctor d ON d.DoctorID = a.DoctorID
JOIN Staff ds ON ds.StaffID = d.DoctorID
ORDER BY a.Date DESC, a.Time DESC;

-- 2. Doctor workload using GROUP BY and COUNT
SELECT
    d.DoctorID,
    CONCAT(s.FirstName, ' ', s.LastName) AS DoctorName,
    dept.DeptName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Doctor d
JOIN Staff s ON s.StaffID = d.DoctorID
JOIN Department dept ON dept.DeptID = d.DeptID
LEFT JOIN Appointment a ON a.DoctorID = d.DoctorID
GROUP BY d.DoctorID, DoctorName, dept.DeptName
ORDER BY TotalAppointments DESC;

-- 3. Revenue by department using SUM and AVG
SELECT
    dept.DeptName,
    COUNT(b.BillID) AS TotalBills,
    SUM(b.Amount) AS TotalRevenue,
    AVG(b.Amount) AS AverageBill
FROM Bill b
JOIN Appointment a ON a.AppointmentID = b.AppointmentID
JOIN Doctor d ON d.DoctorID = a.DoctorID
JOIN Department dept ON dept.DeptID = d.DeptID
GROUP BY dept.DeptName
ORDER BY TotalRevenue DESC;
