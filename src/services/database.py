from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pathlib import Path

Base = declarative_base()


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

    # Relationship to appointments
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete")


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    specialization = Column(String)
    office_number = Column(String)

    # Relationship to appointments
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete")


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    appointment_time = Column(DateTime)
    specialization = Column(String)
    complaints = Column(String)
    diagnosis = Column(String)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class ClinicDatabase:
    def __init__(self, db_path: Path):
        self.engine = create_engine(f'sqlite:///{db_path}', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_patient(self, name: str, phone: str) -> None:
        session = self.Session()
        new_patient = Patient(name=name, phone=phone)
        session.add(new_patient)
        session.commit()
        session.close()

    def delete_patient(self, patient_id) -> None:
        session = self.Session()
        patient = session.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            session.delete(patient)
            session.commit()
        session.close()

    def add_doctor(self, name, phone, specialization, office_number):
        session = self.Session()
        new_doctor = Doctor(name=name, phone=phone, specialization=specialization, office_number=office_number)
        session.add(new_doctor)
        session.commit()
        session.close()

    def delete_doctor(self, doctor_id):
        session = self.Session()
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            session.delete(doctor)
            session.commit()
        session.close()

    def add_appointment(self, patient_id, complaints, specialization):
        session = self.Session()
        new_appointment = Appointment(patient_id=patient_id, appointment_time=datetime.now(),
                                      complaints=complaints, specialization=specialization)
        session.add(new_appointment)
        session.commit()
        session.close()

    def delete_appointment(self, appointment_id):
        session = self.Session()
        appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment:
            session.delete(appointment)
            session.commit()
        session.close()

    def update_diagnosis(self, appointment_id, doctor_id, new_diagnosis):
        session = self.Session()
        appointment = session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment:
            appointment.doctor_id = doctor_id
            appointment.diagnosis = new_diagnosis
            appointment.appointment_time = datetime.now()
            session.commit()
        session.close()

    def get_appointment(self, doctor_id=None, patient_id=None, diagnosis_filter=None, specialization=None):

        session = self.Session()
        query = session.query(Appointment)
        if doctor_id is not None:
            query = query.filter(Appointment.doctor_id == doctor_id)

        if patient_id is not None:
            query = query.filter(Appointment.patient_id == patient_id)

        if specialization is not None:
            query = query.filter(Appointment.specialization == specialization)

        if diagnosis_filter is not None:
            if diagnosis_filter == "with_diagnosis":
                query = query.filter(Appointment.diagnosis != None)
            elif diagnosis_filter == "without_diagnosis":
                query = query.filter(Appointment.diagnosis == None)
        results = query.all()
        session.close()
        return results

    def get_doctor(self, phone=None, doctor_id=None):
        session = self.Session()
        if phone is not None:
            doctor = session.query(Doctor).filter(Doctor.phone == phone).first()

        elif doctor_id is not None:
            doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()

        else:
            doctor = session.query(Doctor)

        session.close()
        return doctor

    def get_patient(self, phone=None, p_id=None):
        session = self.Session()
        query = session.query(Patient)

        if phone is not None:
            query = query.filter(Patient.phone == phone).first()

        elif p_id is not None:
            query = query.filter(Patient.id == p_id).first()

        results = query
        session.close()
        return results

