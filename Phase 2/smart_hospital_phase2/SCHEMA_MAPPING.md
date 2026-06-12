# Schema Mapping Notes

This file explains how the uploaded Smart Hospital Management EERD is implemented.

## Tables

- `Patient`
- `Staff`
- `Doctor`
- `Nurse`
- `Admin`
- `Department`
- `Appointment`
- `Bill`
- `Room`
- `Payment`
- `MedicalRecord`
- `Prescription`
- `PatientRoom`

## Relationships

### Patient Books Appointment

EERD: Patient 1:N Appointment  
Implementation: `Appointment.PatientID` foreign key.

### Doctor Handles Appointment

EERD: Doctor 1:N Appointment  
Implementation: `Appointment.DoctorID` foreign key.

### Admin Schedules Appointment

EERD: Admin 1:N Appointment  
Implementation: `Appointment.AdminID` foreign key.

### Doctor WorksIn Department

EERD: Doctor N:1 Department  
Implementation: `Doctor.DeptID` foreign key with `NOT NULL`.

### Patient Has MedicalRecord

EERD: Identifying 1:N weak entity relationship  
Implementation: `MedicalRecord` has composite primary key `(PatientID, RecordID)`.

### Appointment Generates Prescription

EERD: Identifying 1:N weak entity relationship  
Implementation: `Prescription` has composite primary key `(AppointmentID, PrescriptionID)`.

### Bill ProcessedBy Payment

EERD: Bill 1:1 Payment, total on Payment  
Implementation: `Payment.BillID` is `NOT NULL UNIQUE`.

### Patient AdmittedTo Room

EERD: M:N relationship  
Implementation: associative table `PatientRoom`.

### Nurse Assists Doctor

EERD: Nurse to Doctor relationship  
Implementation: `Doctor.NurseID` foreign key referencing `Nurse`.

## Implementation Note

Some EERD participation constraints such as "every nurse must assist at least one doctor" are difficult to enforce using only a simple foreign key. The implementation supports the relationship and uses foreign keys for integrity, which is acceptable for a Phase 2 CRUD demo.
