from sqlalchemy.orm import sessionmaker
from models import Base, Student, Grade, Subject, Adviser, Distribution, Theme, AdviserGroup, ThemeSubjectImportance, GradeRecord, StudentGradeRecord, StudentThemeInterest

class StudentRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_student(self, firstname, lastname, patronymic, group_student, g):
        session = self.Session()
        new_student = Student(firstname=firstname, lastname=lastname, patronymic=patronymic, group_student=group_student, g=g)
        session.add(new_student)
        session.commit()
        session.close()

    def get_all_students(self):
        session = self.Session()
        students = session.query(Student).all()
        session.close()
        return students

    def get_student_by_id(self, student_id):
        session = self.Session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        session.close()
        return student

    def update_student(self, student_id, firstname=None, lastname=None, patronymic=None, group_student=None, g=None):
        session = self.Session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        if student:
            if firstname: student.firstname = firstname
            if lastname: student.lastname = lastname
            if patronymic: student.patronymic = patronymic
            if group_student: student.group_student = group_student
            if g is not None: student.g = g
            session.commit()
        session.close()

    def delete_student(self, student_id):
        session = self.Session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        if student:
            session.delete(student)
            session.commit()
        session.close()


class GradeRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_grade(self, grade):
        session = self.Session()
        new_grade = Grade(grade=grade)
        session.add(new_grade)
        session.commit()
        session.close()

    def get_all_grades(self):
        session = self.Session()
        grades = session.query(Grade).all()
        session.close()
        return grades

    def get_grade_by_id(self, grade_id):
        session = self.Session()
        grade = session.query(Grade).filter(Grade.grade_id == grade_id).first()
        session.close()
        return grade

    def update_grade(self, grade_id, grade):
        session = self.Session()
        grade_record = session.query(Grade).filter(Grade.grade_id == grade_id).first()
        if grade_record:
            grade_record.grade = grade
            session.commit()
        session.close()

    def delete_grade(self, grade_id):
        session = self.Session()
        grade_record = session.query(Grade).filter(Grade.grade_id == grade_id).first()
        if grade_record:
            session.delete(grade_record)
            session.commit()
        session.close()


class SubjectRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_subject(self, subject_name):
        session = self.Session()
        new_subject = Subject(subject_name=subject_name)
        session.add(new_subject)
        session.commit()
        session.close()

    def get_all_subjects(self):
        session = self.Session()
        subjects = session.query(Subject).all()
        session.close()
        return subjects

    def get_subject_by_id(self, subject_id):
        session = self.Session()
        subject = session.query(Subject).filter(Subject.subject_id == subject_id).first()
        session.close()
        return subject

    def update_subject(self, subject_id, subject_name):
        session = self.Session()
        subject_record = session.query(Subject).filter(Subject.subject_id == subject_id).first()
        if subject_record:
            subject_record.subject_name = subject_name
            session.commit()
        session.close()

    def delete_subject(self, subject_id):
        session = self.Session()
        subject_record = session.query(Subject).filter(Subject.subject_id == subject_id).first()
        if subject_record:
            session.delete(subject_record)
            session.commit()
        session.close()


class AdviserRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_adviser(self, firstname, lastname, patronymic, number_of_places):
        session = self.Session()
        new_adviser = Adviser(firstname=firstname, lastname=lastname, patronymic=patronymic, number_of_places=number_of_places)
        session.add(new_adviser)
        session.commit()
        session.close()

    def get_all_advisers(self):
        session = self.Session()
        advisers = session.query(Adviser).all()
        session.close()
        return advisers

    def get_adviser_by_id(self, adviser_id):
        session = self.Session()
        adviser = session.query(Adviser).filter(Adviser.adviser_id == adviser_id).first()
        session.close()
        return adviser

    def update_adviser(self, adviser_id, firstname=None, lastname=None, patronymic=None, number_of_places=None):
        session = self.Session()
        adviser_record = session.query(Adviser).filter(Adviser.adviser_id == adviser_id).first()
        if adviser_record:
            if firstname: adviser_record.firstname = firstname
            if lastname: adviser_record.lastname = lastname
            if patronymic: adviser_record.patronymic = patronymic
            if number_of_places is not None: adviser_record.number_of_places = number_of_places
            session.commit()
        session.close()

    def delete_adviser(self, adviser_id):
        session = self.Session()
        adviser_record = session.query(Adviser).filter(Adviser.adviser_id == adviser_id).first()
        if adviser_record:
            session.delete(adviser_record)
            session.commit()
        session.close()


class DistributionRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_distribution(self, theme_subject_importance_id, student_grade_record_id, student_theme_interest_id):
        session = self.Session()
        new_distribution = Distribution(theme_subject_importance_id=theme_subject_importance_id, student_grade_record_id=student_grade_record_id, student_theme_interest_id=student_theme_interest_id)
        session.add(new_distribution)
        session.commit()
        session.close()

    def get_all_distributions(self):
        session = self.Session()
        distributions = session.query(Distribution).all()
        session.close()
        return distributions

    def get_distribution_by_id(self, distribution_id):
        session = self.Session()
        distribution = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
        session.close()
        return distribution

    def update_distribution(self, distribution_id, theme_subject_importance_id=None, student_grade_record_id=None, student_theme_interest_id=None):
        session = self.Session()
        distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
        if distribution_record:
            if theme_subject_importance_id is not None: distribution_record.theme_subject_importance_id = theme_subject_importance_id
            if student_grade_record_id is not None: distribution_record.student_grade_record_id = student_grade_record_id
            if student_theme_interest_id is not None: distribution_record.student_theme_interest_id = student_theme_interest_id
            session.commit()
        session.close()

    def delete_distribution(self, distribution_id):
        session = self.Session()
        distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
        if distribution_record:
            session.delete(distribution_record)
            session.commit()
        session.close()


class ThemeRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_theme(self, theme_name, interest_level, adviser_group_id):
        session = self.Session()
        new_theme = Theme(theme_name=theme_name, interest_level=interest_level, adviser_group_id=adviser_group_id)
        session.add(new_theme)
        session.commit()
        session.close()

    def get_all_themes(self):
        session = self.Session()
        themes = session.query(Theme).all()
        session.close()
        return themes

    def get_theme_by_id(self, theme_id):
        session = self.Session()
        theme = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        session.close()
        return theme

    def update_theme(self, theme_id, theme_name=None, interest_level=None, adviser_group_id=None):
        session = self.Session()
        theme_record = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        if theme_record:
            if theme_name: theme_record.theme_name = theme_name
            if interest_level is not None: theme_record.interest_level = interest_level
            if adviser_group_id is not None: theme_record.adviser_group_id = adviser_group_id
            session.commit()
        session.close()

    def delete_theme(self, theme_id):
        session = self.Session()
        theme_record = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        if theme_record:
            session.delete(theme_record)
            session.commit()
        session.close()


class AdviserGroupRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_adviser_group(self, adviser_id, group_specialization):
        session = self.Session()
        new_adviser_group = AdviserGroup(adviser_id=adviser_id, group_specialization=group_specialization)
        session.add(new_adviser_group)
        session.commit()
        session.close()

    def get_all_adviser_groups(self):
        session = self.Session()
        adviser_groups = session.query(AdviserGroup).all()
        session.close()
        return adviser_groups

    def get_adviser_group_by_id(self, adviser_group_id):
        session = self.Session()
        adviser_group = session.query(AdviserGroup).filter(AdviserGroup.adviser_group_id == adviser_group_id).first()
        session.close()
        return adviser_group

    def update_adviser_group(self, adviser_group_id, adviser_id=None, group_specialization=None):
        session = self.Session()
        adviser_group_record = session.query(AdviserGroup).filter(AdviserGroup.adviser_group_id == adviser_group_id).first()
        if adviser_group_record:
            if adviser_id is not None: adviser_group_record.adviser_id = adviser_id
            if group_specialization: adviser_group_record.group_specialization = group_specialization
            session.commit()
        session.close()

    def delete_adviser_group(self, adviser_group_id):
        session = self.Session()
        adviser_group_record = session.query(AdviserGroup).filter(AdviserGroup.adviser_group_id == adviser_group_id).first()
        if adviser_group_record:
            session.delete(adviser_group_record)
            session.commit()
        session.close()


class ThemeSubjectImportanceRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_theme_subject_importance(self, theme_id, subject_id, weight):
        session = self.Session()
        new_theme_subject_importance = ThemeSubjectImportance(theme_id=theme_id, subject_id=subject_id, weight=weight)
        session.add(new_theme_subject_importance)
        session.commit()
        session.close()

    def get_all_theme_subject_importances(self):
        session = self.Session()
        theme_subject_importances = session.query(ThemeSubjectImportance).all()
        session.close()
        return theme_subject_importances

    def get_theme_subject_importance_by_id(self, theme_subject_importance_id):
        session = self.Session()
        theme_subject_importance = session.query(ThemeSubjectImportance).filter(ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        session.close()
        return theme_subject_importance

    def update_theme_subject_importance(self, theme_subject_importance_id, theme_id=None, subject_id=None, weight=None):
        session = self.Session()
        theme_subject_importance_record = session.query(ThemeSubjectImportance).filter(ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        if theme_subject_importance_record:
            if theme_id is not None: theme_subject_importance_record.theme_id = theme_id
            if subject_id is not None: theme_subject_importance_record.subject_id = subject_id
            if weight is not None: theme_subject_importance_record.weight = weight
            session.commit()
        session.close()

    def delete_theme_subject_importance(self, theme_subject_importance_id):
        session = self.Session()
        theme_subject_importance_record = session.query(ThemeSubjectImportance).filter(ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        if theme_subject_importance_record:
            session.delete(theme_subject_importance_record)
            session.commit()
        session.close()


class GradeRecordRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_grade_record(self, subject_id, grade_id):
        session = self.Session()
        new_grade_record = GradeRecord(subject_id=subject_id, grade_id=grade_id)
        session.add(new_grade_record)
        session.commit()
        session.close()

    def get_all_grade_records(self):
        session = self.Session()
        grade_records = session.query(GradeRecord).all()
        session.close()
        return grade_records

    def get_grade_record_by_id(self, grade_record_id):
        session = self.Session()
        grade_record = session.query(GradeRecord).filter(GradeRecord.grade_record_id == grade_record_id).first()
        session.close()
        return grade_record

    def update_grade_record(self, grade_record_id, subject_id=None, grade_id=None):
        session = self.Session()
        grade_record_record = session.query(GradeRecord).filter(GradeRecord.grade_record_id == grade_record_id).first()
        if grade_record_record:
            if subject_id is not None: grade_record_record.subject_id = subject_id
            if grade_id is not None: grade_record_record.grade_id = grade_id
            session.commit()
        session.close()

    def delete_grade_record(self, grade_record_id):
        session = self.Session()
        grade_record_record = session.query(GradeRecord).filter(GradeRecord.grade_record_id == grade_record_id).first()
        if grade_record_record:
            session.delete(grade_record_record)
            session.commit()
        session.close()


class StudentGradeRecordRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_student_grade_record(self, student_id, grade_record_id):
        session = self.Session()
        new_student_grade_record = StudentGradeRecord(student_id=student_id, grade_record_id=grade_record_id)
        session.add(new_student_grade_record)
        session.commit()
        session.close()

    def get_all_student_grade_records(self):
        session = self.Session()
        student_grade_records = session.query(StudentGradeRecord).all()
        session.close()
        return student_grade_records

    def get_student_grade_record_by_id(self, student_grade_record_id):
        session = self.Session()
        student_grade_record = session.query(StudentGradeRecord).filter(StudentGradeRecord.student_grade_record_id == student_grade_record_id).first()
        session.close()
        return student_grade_record

    def update_student_grade_record(self, student_grade_record_id, student_id=None, grade_record_id=None):
        session = self.Session()
        student_grade_record_record = session.query(StudentGradeRecord).filter(StudentGradeRecord.student_grade_record_id == student_grade_record_id).first()
        if student_grade_record_record:
            if student_id is not None: student_grade_record_record.student_id = student_id
            if grade_record_id is not None: student_grade_record_record.grade_record_id = grade_record_id
            session.commit()
        session.close()

    def delete_student_grade_record(self, student_grade_record_id):
        session = self.Session()
        student_grade_record_record = session.query(StudentGradeRecord).filter(StudentGradeRecord.student_grade_record_id == student_grade_record_id).first()
        if student_grade_record_record:
            session.delete(student_grade_record_record)
            session.commit()
        session.close()


class StudentThemeInterestRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_student_theme_interest(self, student_id, theme_id, interest_level):
        session = self.Session()
        new_student_theme_interest = StudentThemeInterest(student_id=student_id, theme_id=theme_id, interest_level=interest_level)
        session.add(new_student_theme_interest)
        session.commit()
        session.close()

    def get_all_student_theme_interests(self):
        session = self.Session()
        student_theme_interests = session.query(StudentThemeInterest).all()
        session.close()
        return student_theme_interests

    def get_student_theme_interest_by_id(self, student_theme_interest_id):
        session = self.Session()
        student_theme_interest = session.query(StudentThemeInterest).filter(StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        session.close()
        return student_theme_interest

    def update_student_theme_interest(self, student_theme_interest_id, student_id=None, theme_id=None, interest_level=None):
        session = self.Session()
        student_theme_interest_record = session.query(StudentThemeInterest).filter(StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        if student_theme_interest_record:
            if student_id is not None: student_theme_interest_record.student_id = student_id
            if theme_id is not None: student_theme_interest_record.theme_id = theme_id
            if interest_level is not None: student_theme_interest_record.interest_level = interest_level
            session.commit()
        session.close()

    def delete_student_theme_interest(self, student_theme_interest_id):
        session = self.Session()
        student_theme_interest_record = session.query(StudentThemeInterest).filter(StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        if student_theme_interest_record:
            session.delete(student_theme_interest_record)
            session.commit()
        session.close()