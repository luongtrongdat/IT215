from sqlalchemy import Column,Integer,String,Date,ForeignKey,Table
from sqlalchemy.orm import relationship
from database.database import Base

# Quan hệ N-N giữa Patient và Medication
patient_medication = Table(
    "patient_medication",
    Base.metadata,
    Column("patient_id",Integer,ForeignKey("patients.id"),primary_key=True),
    Column("medication_id",Integer,ForeignKey("medications.id"),primary_key=True)
)

# DOCTOR
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    specialty = Column(String(100),nullable=False)
    # Quan hệ 1-N với Patient
    patients = relationship("Patient",back_populates="doctor")

# PATIENT
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer,primary_key=True,index=True)
    patient_code = Column(String(50),unique=True,nullable=False,index=True)
    doctor_id = Column(Integer,ForeignKey("doctors.id"),nullable=False)
    # Quan hệ N-1 với Doctor
    doctor = relationship("Doctor",back_populates="patients")
    # Quan hệ 1-1 với Insurance
    insurance = relationship("Insurance",back_populates="patient",uselist=False)
    # Quan hệ N-N với Medication
    medications = relationship("Medication",secondary=patient_medication,back_populates="patients")

# INSURANCE
class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(Integer,primary_key=True,index=True)
    insurance_number = Column(String(100),unique=True,nullable=False)
    expiry_date = Column(Date,nullable=False)
    patient_id = Column(Integer,ForeignKey("patients.id"),unique=True,nullable=False)
    # Quan hệ 1-1 với Patient
    patient = relationship("Patient",back_populates="insurance")

# MEDICATION
class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    # Quan hệ N-N với Patient
    patients = relationship("Patient",secondary=patient_medication,back_populates="medications")