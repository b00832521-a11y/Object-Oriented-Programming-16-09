# UML exo 1 - Hospital Management System - Task 3 (sequence diagrams)

Statement: system sequence diagrams for 3 scenarios.

![Task 3 sequence diagrams](exo1_task3_sequences.jpg)

## 1. Patient Registration (Organizer creates a new member)
Participants: NewMember, Organizer, System.
askJoin -> create(name, role) -> generatePassword() / save(member) (self calls) -> sendInfos(id, pass) -> login(id, pass) -> access granted.

## 2. Consultation Flow (problem submission to prescription delivery)
Participants: Patient, Organizer, HealthProblem, Doctor.
postProblem -> create (PENDING) -> updateStatus(IN_REVIEW) -> consultDoctor -> providePrescription (return) -> updateStatus(RESOLVED) -> sendPrescription to the patient.

## 3. Payment Processing (patient pays, Organizer forwards to doctor)
Participants: Patient, Organizer, Payment, Doctor.
pay(amount) -> create(amount, type) -> process() -> confirmed (return) -> forwardPayment(amount) to the doctor.
