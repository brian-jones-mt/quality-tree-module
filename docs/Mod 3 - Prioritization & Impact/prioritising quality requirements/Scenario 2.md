### **Scenario 2: Healthcare Management System (e.g., Electronic Health Records)**

1. **Security:** Patient data access must be HIPAA compliant and auditable.
2. **Performance:** Retrieving a patient's full medical history must take less than 1 second.
3. **Reliability:** System must be available 24/7 with minimal downtime for critical functions.
4. **Scalability:** Must support a growing number of hospitals and clinics, each with thousands of patients.
5. **Interoperability:** Ability to exchange patient data with external lab systems using FHIR standards.
6. **Data Integrity:** Prevent unauthorized alteration of patient records.
7. **Usability:** Doctors must be able to input consultation notes quickly and efficiently.
8. **Maintainability:** Updates to medical coding standards (e.g., ICD-10) should be easily configurable.
9. **Auditability:** All user actions on patient records must be logged.
10. **Backup & Recovery:** Backups with a 1-hour RTO and 30-minute RPO.
11. **Authentication:** Support multi-factor authentication for all users.
12. **Response Time:** Critical alerts for patient vitals must be delivered within 500ms.
