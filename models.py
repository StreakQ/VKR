from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    group_student = Column(String, nullable=False)

    grades = relationship("StudentSubjectGrade", back_populates="student")
    interests = relationship("StudentThemeInterest", back_populates="student")

class Adviser(Base):
    __tablename__ = 'advisers'
    adviser_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    number_of_places = Column(Integer, nullable=False)

    adviser_group = relationship("AdviserGroup", back_populates="adviser")

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String, nullable=False)

    subject_importances = relationship("ThemeSubjectImportance", back_populates="subject")
    student_subject_grades = relationship("StudentSubjectGrade", back_populates="subject")

class Theme(Base):
    __tablename__ = 'themes'
    theme_id = Column(Integer, primary_key=True)
    theme_name = Column(String, nullable=False)

    subject_importances = relationship("ThemeSubjectImportance", back_populates="theme")
    student_theme_interests = relationship("StudentThemeInterest", back_populates="theme")

class AdviserGroup(Base):
    __tablename__ = 'adviser_groups'
    adviser_group_id = Column(Integer, primary_key=True)
    adviser_id = Column(Integer, ForeignKey('advisers.adviser_id'), unique=True, nullable=False)
    group_specialization = Column(String, nullable=False)

    adviser = relationship("Adviser", back_populates="adviser_group")


class ThemeSubjectImportance(Base):
    __tablename__ = 'theme_subject_importances'
    theme_subject_importance_id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    weight = Column(Float, nullable=False)

    theme = relationship("Theme", back_populates="subject_importances")
    subject = relationship("Subject", back_populates="subject_importances")

class StudentSubjectGrade(Base):
    __tablename__ = 'student_subjects_grades'
    student_subject_grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    grade = Column(Float, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="student_subject_grades")

class StudentThemeInterest(Base):
    __tablename__ = 'student_theme_interests'
    student_theme_interest_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'), nullable=False)
    interest_level = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="interests")
    theme = relationship("Theme", back_populates="student_theme_interests")

class Distribution(Base):
    __tablename__ = 'distributions'

    distribution_id = Column(Integer, primary_key=True)
    theme_subject_importance_id = Column(Integer, ForeignKey('theme_subject_importances.theme_subject_importance_id'), nullable=False)
    student_subject_grade_id = Column(Integer, ForeignKey('student_subjects_grades.student_subject_grade_id'), nullable=False)
    student_theme_interest_id = Column(Integer, ForeignKey('student_theme_interests.student_theme_interest_id'), nullable=False)

    theme_subject_importance = relationship("ThemeSubjectImportance")
    student_grade_record = relationship("StudentSubjectGrade")
    student_theme_interest = relationship("StudentThemeInterest")
