import sqlite3
from models import Patient, Doctor

class Database:
    def __init__(self, db_name="hospital.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                diagnosis TEXT NOT NULL,
                doctor_id INTEGER, FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        """)
        self.conn.commit()

    #ექიმზე მეთოდები
    def fetch_doctors(self):
        self.cursor.execute("SELECT * FROM doctors")
        rows = self.cursor.fetchall()
        return [Doctor(*row) for row in rows]

    def insert_doctor(self, doctor: Doctor):
        self.cursor.execute(
            "INSERT INTO doctors (name, specialty) VALUES (?, ?)",
            doctor.as_tuple()
        )
        self.conn.commit()

    def update_doctor(self, doctor: Doctor):
        self.cursor.execute(
            "UPDATE doctors SET name=?, specialty=? WHERE id=?",
            (doctor.name, doctor.specialty, doctor.id)
        )
        self.conn.commit()

    def delete_doctor(self, doctor_id):
        self.cursor.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
        self.conn.commit()

    #პაციენტზე მეთოდები
    def fetch_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        rows = self.cursor.fetchall()
        return [Patient(*row) for row in rows]

    def insert_patient(self, patient: Patient):
        self.cursor.execute(
            "INSERT INTO patients (name, age, diagnosis, doctor_id) VALUES (?, ?, ?, ?)",
            patient.as_tuple()
        )
        self.conn.commit()

    def update_patient(self, patient: Patient):
        self.cursor.execute(
            "UPDATE patients SET name=?, age=?, diagnosis=?, doctor_id=? WHERE id=?",
            (patient.name, patient.age, patient.diagnosis, patient.doctor_id, patient.id)
        )
        self.conn.commit()

    def delete_patient(self, patient_id):
        self.cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

