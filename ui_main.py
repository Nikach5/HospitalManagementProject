from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit,
    QPushButton, QLabel, QMessageBox, QTabWidget
)
from models import Patient, Doctor

class MainWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Hospital Management")
        self.setGeometry(100, 100, 500, 400)

        self.tabs = QTabWidget(self)

        #პაციენტების ტაბი
        self.patient_tab = QWidget()
        self.patient_list = QListWidget()
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.diagnosis_input = QLineEdit()
        self.add_patient_btn = QPushButton("Add Patient")
        self.update_patient_btn = QPushButton("Update Patient")
        self.delete_patient_btn = QPushButton("Delete Patient")

        p_layout = QVBoxLayout()
        p_form = QHBoxLayout()
        p_buttons = QHBoxLayout()

        p_form.addWidget(QLabel("Name:"))
        p_form.addWidget(self.name_input)
        p_form.addWidget(QLabel("Age:"))
        p_form.addWidget(self.age_input)
        p_form.addWidget(QLabel("Diagnosis:"))
        p_form.addWidget(self.diagnosis_input)

        p_buttons.addWidget(self.add_patient_btn)
        p_buttons.addWidget(self.update_patient_btn)
        p_buttons.addWidget(self.delete_patient_btn)

        p_layout.addWidget(self.patient_list)
        p_layout.addLayout(p_form)
        p_layout.addLayout(p_buttons)
        self.patient_tab.setLayout(p_layout)
        self.tabs.addTab(self.patient_tab, "Patients")

        # ექიმების ტაბი
        self.doctor_tab = QWidget()
        self.doctor_list = QListWidget()
        self.doctor_name_input = QLineEdit()
        self.doctor_spec_input = QLineEdit()
        self.add_doctor_btn = QPushButton("Add Doctor")
        self.update_doctor_btn = QPushButton("Update Doctor")
        self.delete_doctor_btn = QPushButton("Delete Doctor")

        d_layout = QVBoxLayout()
        d_form = QHBoxLayout()
        d_buttons = QHBoxLayout()

        d_form.addWidget(QLabel("Name:"))
        d_form.addWidget(self.doctor_name_input)
        d_form.addWidget(QLabel("Specialty:"))
        d_form.addWidget(self.doctor_spec_input)

        d_buttons.addWidget(self.add_doctor_btn)
        d_buttons.addWidget(self.update_doctor_btn)
        d_buttons.addWidget(self.delete_doctor_btn)

        d_layout.addWidget(self.doctor_list)
        d_layout.addLayout(d_form)
        d_layout.addLayout(d_buttons)
        self.doctor_tab.setLayout(d_layout)
        self.tabs.addTab(self.doctor_tab, "Doctors")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.add_patient_btn.clicked.connect(self.add_patient)
        self.update_patient_btn.clicked.connect(self.update_patient)
        self.delete_patient_btn.clicked.connect(self.delete_patient)
        self.patient_list.itemSelectionChanged.connect(self.fill_patient_form)

        self.add_doctor_btn.clicked.connect(self.add_doctor)
        self.update_doctor_btn.clicked.connect(self.update_doctor)
        self.delete_doctor_btn.clicked.connect(self.delete_doctor)
        self.doctor_list.itemSelectionChanged.connect(self.fill_doctor_form)

        self.load_data()

    def load_data(self):
        self.patient_list.clear()
        self.doctor_list.clear()

        self.patients = self.db.fetch_patients()
        self.doctors = self.db.fetch_doctors()

        for p in self.patients:
            self.patient_list.addItem(f"{p.id}: {p.name}, Age: {p.age}, Diagnosis: {p.diagnosis}")

        for d in self.doctors:
            self.doctor_list.addItem(f"{d.id}: {d.name}, {d.specialty}")

    #პაციენტები
    def fill_patient_form(self):
        selected = self.patient_list.currentItem()
        if not selected:
            return
        patient_id = int(selected.text().split(":")[0])
        for p in self.patients:
            if p.id == patient_id:
                self.name_input.setText(p.name)
                self.age_input.setText(str(p.age))
                self.diagnosis_input.setText(p.diagnosis)
                break

    def add_patient(self):
        name = self.name_input.text()
        age = self.age_input.text()
        diagnosis = self.diagnosis_input.text()
        if not name or not age or not diagnosis:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, "Error", "Age must be a number.")
            return
        patient = Patient(None, name, age, diagnosis)
        self.db.insert_patient(patient)
        self.load_data()

    def update_patient(self):
        selected = self.patient_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a patient to update.")
            return
        patient_id = int(selected.text().split(":")[0])
        name = self.name_input.text()
        age = self.age_input.text()
        diagnosis = self.diagnosis_input.text()
        if not name or not age or not diagnosis:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, "Error", "Age must be a number.")
            return
        patient = Patient(patient_id, name, age, diagnosis)
        self.db.update_patient(patient)
        self.load_data()

    def delete_patient(self):
        selected = self.patient_list.currentItem()
        if not selected:
            return
        patient_id = int(selected.text().split(":")[0])
        self.db.delete_patient(patient_id)
        self.load_data()

    #ექიმები
    def fill_doctor_form(self):
        selected = self.doctor_list.currentItem()
        if not selected:
            return
        doctor_id = int(selected.text().split(":")[0])
        for d in self.doctors:
            if d.id == doctor_id:
                self.doctor_name_input.setText(d.name)
                self.doctor_spec_input.setText(d.specialty)
                break

    def add_doctor(self):
        name = self.doctor_name_input.text()
        specialty = self.doctor_spec_input.text()
        if not name or not specialty:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        doctor = Doctor(None, name, specialty)
        self.db.insert_doctor(doctor)
        self.load_data()

    def update_doctor(self):
        selected = self.doctor_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a doctor to update.")
            return
        doctor_id = int(selected.text().split(":")[0])
        name = self.doctor_name_input.text()
        specialty = self.doctor_spec_input.text()
        if not name or not specialty:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        doctor = Doctor(doctor_id, name, specialty)
        self.db.update_doctor(doctor)
        self.load_data()

    def delete_doctor(self):
        selected = self.doctor_list.currentItem()
        if not selected:
            return
        doctor_id = int(selected.text().split(":")[0])
        self.db.delete_doctor(doctor_id)
        self.load_data()
