class Patient:
    def __init__(self, patient_id, name, age, diagnosis, doctor_id=None):
        self.id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.doctor_id = doctor_id

    def __str__(self):
        return f"Patient ID: {self.id}, Name: {self.name}, Age: {self.age}, Diagnosis: {self.diagnosis}"

    def as_tuple(self):
        return (self.name, self.age, self.diagnosis, self.doctor_id)



class Doctor:
    def __init__(self, doctor_id, name, specialty):
        self.id = doctor_id
        self.name = name
        self.specialty = specialty

    def __str__(self):
        return f"{self.name} ({self.specialty})"

    def as_tuple(self):
        return (self.name, self.specialty)


