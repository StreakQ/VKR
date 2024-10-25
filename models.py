from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    group_student = Column(String, nullable=False)
    g = Column(Integer, nullable=False)

class Adviser(Base):
    __tablename__ = 'advisers'
    adviser_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    number_of_places = Column(Integer, nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String, nullable=False)

class Distribution(Base):
    __tablename__ = 'distributions'
    distribution_id = Column(Integer, primary_key=True)
    theme_subject_importance_id = Column(Integer, ForeignKey('theme_subject_importance.theme_subject_importance_id'), nullable=False)
    student_grade_record_id = Column(Integer, ForeignKey('student_grade_records.student_grade_record_id'), nullable=False)
    student_theme_interest_id = Column(Integer, ForeignKey('student_theme_interests.student_theme_interest_id'), nullable=False)

class Theme(Base):
    __tablename__ = 'themes'
    theme_id = Column(Integer, primary_key=True)
    theme_name = Column(String, nullable=False)
    interest_level = Column(Integer, nullable=False)
    adviser_group_id = Column(Integer, ForeignKey('adviser_groups.adviser_group_id'), nullable=False)

class AdviserGroup(Base):
    __tablename__ = 'adviser_groups'
    adviser_group_id = Column(Integer, primary_key=True)
    adviser_id = Column(Integer, ForeignKey('advisers.adviser_id'), unique=True, nullable=False)
    group_specialization = Column(String, nullable=False)

class ThemeSubjectImportance(Base):
    __tablename__ = 'theme_subject_importance'
    theme_subject_importance_id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    weight = Column(Float, nullable=False)

    # Определение отношений
    theme = relationship("Theme", back_populates="subject_importances")
    subject = relationship("Subject", back_populates="subject_importances")

class GradeRecord(Base):
    __tablename__ = 'grade_records'
    grade_record_id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    grade_id = Column(Integer, ForeignKey('grades.grade_id'), nullable=False)

class StudentGradeRecord(Base):
    __tablename__ = 'student_grade_records'
    student_grade_record_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    grade_record_id = Column(Integer, ForeignKey('grade_records.grade_record_id'), nullable=False)

    # Определение отношений
    student = relationship("Student")
    grade_record = relationship("GradeRecord")

class StudentThemeInterest(Base):
    __tablename__ = 'student_theme_interests'
    student_theme_interest_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'), nullable=False)
    interest_level = Column(Integer, nullable=False)

# Определение связей между сущностями
Theme.subject_importances = relationship("ThemeSubjectImportance", back_populates="theme")
Subject.subject_importances = relationship("ThemeSubjectImportance", back_populates="subject")
Distribution.theme_subject_importance = relationship("ThemeSubjectImportance")
Distribution.student_grade_record = relationship("StudentGradeRecord")
Distribution.student_theme_interest = relationship("StudentThemeInterest")
AdviserGroup.adviser = relationship("Adviser")
Adviser.adviser_group = relationship("AdviserGroup", back_populates="adviser")
