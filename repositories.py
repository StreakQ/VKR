from sqlalchemy.orm import sessionmaker
from models import (Student, Adviser, Subject, Theme, AdviserGroup,
                    ThemeSubjectImportance, StudentSubjectGrade, StudentThemeInterest, Distribution, ThemeAdviserGroup)
from faker import Faker
import  random as rnd

fake = Faker('ru_RU')


class StudentRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_student(self, firstname, lastname, patronymic, group_student):
        session = self.Session()
        new_student = Student(firstname=firstname, lastname=lastname, patronymic=patronymic, group_student=group_student)
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

    def update_student(self, student_id, firstname=None, lastname=None, patronymic=None, group_student=None):
        session = self.Session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        if student:
            if firstname: student.firstname = firstname
            if lastname: student.lastname = lastname
            if patronymic: student.patronymic = patronymic
            if group_student: student.group_student = group_student
            session.commit()
        session.close()

    def delete_student(self, student_id):
        session = self.Session()
        student = session.query(Student).filter(Student.student_id == student_id).first()
        if student:
            session.delete(student)
            session.commit()
        session.close()

    def add_initial_students(self, count=10):
        for _ in range(count):
            self.add_student(fake.first_name_male(), fake.last_name_male(), fake.first_name_male(),
                             f"A-{fake.random_int(1, 3)}-21")

    def display_all_students(self):
        students = self.get_all_students()
        for student in students:
            print(
                f"ID Студента: {student.student_id}, Имя: {student.firstname} {student.lastname}, "
                f"Группа: {student.group_student}")

    def delete_all_students(self):
        session = self.Session()
        try:
            session.query(Student).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
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

    def add_initial_advisers(self, count=5):
        for _ in range(count):
            self.add_adviser(fake.first_name_male(), fake.last_name_male(), fake.first_name_male(),
                             fake.random_int(min=1, max=10))

    def display_all_advisers(self):
        advisers = self.get_all_advisers()
        for adviser in advisers:
            print(
                f"ID Руководителя: {adviser.adviser_id}, Имя: {adviser.firstname} {adviser.lastname}, Мест: "
                f"{adviser.number_of_places}")

    def delete_all_advisers(self):
        session = self.Session()
        try:
            session.query(Adviser).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
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
        subject_record = session.query(Subject).filter( Subject.subject_id == subject_id).first()
        if subject_record:
            session.delete(subject_record)
            session.commit()
        session.close()

    @staticmethod
    def choose_unique_value(lst):
        if not lst:
            return None
        random_value = rnd.choice(lst)
        lst.remove(random_value)
        return random_value

    def add_initial_subjects(self, count=5):
        subjects_list = [
            "Алгебра и аналитическая геометрия",
            "Математический анализ",
            "Математический анализ, часть 2 ",
            "Программирование и основы алгоритмизации",
            "Физика ",
            "Разработка программного обеспечения систем управления",
            "Вычислительные методы",
            "Статистические методы в инженерных исследованиях",
            "Электротехника ",
            "Методы оптимизации",
            "Информационные технологии ",
            "Программное обеспечение автоматизированных систем",
            "Элементы и системы пневмоавтоматики",
            "Интеллектуальный анализ данных",
            "Функциональные узлы и схемотехника систем управления и вычислительных машин",
            "Системное программное обеспечение",
            "Элементы и системы гидроавтоматики",
            "Нейрокомпьютеры и их применение"
        ]
        for _ in range(count):
            self.add_subject(self.choose_unique_value(subjects_list))

    def display_all_subjects(self):
        subjects = self.get_all_subjects()
        for subject in subjects:
            print(f"ID Предмета: {subject.subject_id}, Название: {subject.subject_name}")

    def delete_all_subjects(self):
        session = self.Session()
        try:
            session.query(Subject).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

class ThemeRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def add_theme(self, theme_name):
        session = self.Session()
        new_theme = Theme(theme_name=theme_name)
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

    def update_theme(self, theme_id, theme_name=None):
        session = self.Session()
        theme_record = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        if theme_record:
            if theme_name: theme_record.theme_name = theme_name
            session.commit()
        session.close()

    def delete_theme(self, theme_id):
        session = self.Session()
        theme_record = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        if theme_record:
            session.delete(theme_record)
            session.commit()
        session.close()

    def update_adviser_group_for_theme(self, theme_id, adviser_group_id):
        session = self.Session()
        theme_record = session.query(Theme).filter(Theme.theme_id == theme_id).first()
        if theme_record:
            theme_record.adviser_group_id = adviser_group_id
            session.commit()
        session.close()

    @staticmethod
    def choose_unique_value(lst):
        if not lst:
            return None
        random_value = rnd.choice(lst)
        lst.remove(random_value)
        return random_value

    def add_initial_themes(self, count=5):
        themes = [
            "Разработка методов декомпозиции сложных моделей многотемповых динамических систем",
            "Исследование и разработка алгоритмов управления сложными динамическими объектами",
            "Структурная и параметрическая идентификация динамических объектов",
            "Разработка методов нечеткой логики и нейро-нечетких алгоритмов диагностики динамических объектов и управления ими",
            "Робототехнические системы, нейро-нечеткие алгоритмы управления",
            "Разработка систем компьютерного зрения при управлении динамическими объектами",
            "Разработка учебно-исследовательских лабораторных комплексов по дисциплинам кафедры на базе стандартных программных средств",
            "Микропроцессорные и аппаратно-технические средства систем управления и автоматизации",
            "Автоматизация технологических процессов",
            "Нейросетевые системы управления и их применение",
            "Машинное обучение и интеллектуальный анализ данных",
            "Нейросетевые методы обработки данных",
            "Методы распознавания образов, текста и речи",
            "Анализ стохастических процессов, разработка методов прогнозирования стационарных и нестационарных временных рядов",
            "Методы, модели и методики обеспечения информационной безопасности компьютерных систем",
            "Разработка информационных систем с использованием баз данных",
            "Методы и программные средства анализа данных при поддержке принятия решений",
            "Разработка систем диспетчеризации (SCADA-системы)",
            "Разработка цифровых систем на основе ЭВМ для сбора и обработки данных",
            "Разработка систем автоматизации на основе одноплатных ЭВМ"
        ]
        for _ in range(count):
            theme_name = self.choose_unique_value(themes)
            self.add_theme(theme_name)

    def display_all_themes(self):
        themes = self.get_all_themes()
        for theme in themes:
            print(f"ID Темы: {theme.theme_id}, Название: {theme.theme_name}")

    def delete_all_themes(self):
        session = self.Session()
        try:
            session.query(Theme).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


class AdviserGroupRepository:
    def __init__(self, engine, adviser_repository):
        self.Session = sessionmaker(bind=engine)
        self.adviser_repository = adviser_repository

    def add_adviser_in_group(self, adviser_id, group_specialization):
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

    def update_adviser_group(self, adviser_group_id, adviser_id=None, specialization=None):
        session = self.Session()
        adviser_group_record = session.query(AdviserGroup).filter(AdviserGroup.adviser_group_id == adviser_group_id).first()
        if adviser_group_record:
            if adviser_id is not None: adviser_group_record.adviser_id = adviser_id
            if specialization: adviser_group_record.group_specialization = specialization
            session.commit()
        session.close()



    def delete_adviser_group(self, adviser_group_id):
        session = self.Session()
        adviser_group_record = session.query(AdviserGroup).filter(AdviserGroup.adviser_group_id == adviser_group_id).first()
        if adviser_group_record:
            session.delete(adviser_group_record)
            session.commit()
        session.close()

    def display_all_adviser_groups(self):
        adviser_groups = self.get_all_adviser_groups()
        for group in adviser_groups:
            print(
                f"ID Группы руководителей: {group.adviser_group_id}, ID Руководителя: {group.adviser_id}, "
                f"Специализация: {group.group_specialization}")

    def init_all_adviser_groups(self, advisers):
        group_specializations = ["Специализация 1", "Специализация 2"]
        for adviser in advisers:
            specialization = rnd.choice(group_specializations)
            self.add_adviser_in_group(adviser.adviser_id, specialization)


    def delete_all_adviser_groups(self):
        session = self.Session()
        try:
            session.query(AdviserGroup).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

class ThemeAdviserGroupRepository:
    def __init__(self, engine, theme_repo, adviser_group_repo):
        self.Session = sessionmaker(bind=engine)
        self.theme_repo = theme_repo
        self.adviser_group_repo = adviser_group_repo

    def add_theme_adviser_group(self, theme_id, adviser_group_id):
        session = self.Session()
        try:
            new_relation = ThemeAdviserGroup(theme_id=theme_id, adviser_group_id=adviser_group_id)
            session.add(new_relation)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении связи темы и группы советников: {e}")
        finally:
            session.close()

    def get_all_theme_adviser_groups(self):
        session = self.Session()
        relations = session.query(ThemeAdviserGroup).all()
        session.close()
        return relations

    def get_theme_adviser_group_by_id(self, theme_adviser_group_id):
        session = self.Session()
        relation = session.query(ThemeAdviserGroup).filter(ThemeAdviserGroup.theme_adviser_group_id == theme_adviser_group_id).first()
        session.close()
        return relation

    def get_adviser_group_by_theme(self, theme_id):
        session = self.Session()
        try:
            relation = session.query(ThemeAdviserGroup).filter(ThemeAdviserGroup.theme_id == theme_id).first()
            return relation
        finally:
            session.close()

    def update_theme_adviser_group(self, theme_adviser_group_id, theme_id=None, adviser_group_id=None):
        session = self.Session()
        relation = session.query(ThemeAdviserGroup).filter(ThemeAdviserGroup.theme_adviser_group_id == theme_adviser_group_id).first()
        if relation:
            if theme_id is not None:
                relation.theme_id = theme_id
            if adviser_group_id is not None:
                relation.adviser_group_id = adviser_group_id
            session.commit()
        session.close()

    def delete_theme_adviser_group(self, theme_adviser_group_id):
        session = self.Session()
        relation = session.query(ThemeAdviserGroup).filter(ThemeAdviserGroup.theme_adviser_group_id == theme_adviser_group_id).first()
        if relation:
            session.delete(relation)
            session.commit()
        session.close()

    def populate_theme_adviser_groups(self):
        themes = self.theme_repo.get_all_themes()
        adviser_groups = self.adviser_group_repo.get_all_adviser_groups()

        if not themes or not adviser_groups:
            print("Нет доступных тем или групп советников для заполнения.")
            return

        for theme in themes:
            # Случайно выбираем группу советников
            adviser_group = rnd.choice(adviser_groups)
            self.add_theme_adviser_group(theme.theme_id, adviser_group.adviser_group_id)
            print(f"Связь добавлена: Тема ID {theme.theme_id} - Группа советников ID {adviser_group.adviser_group_id}")



    def display_all_theme_adviser_groups(self):
        relations = self.get_all_theme_adviser_groups()
        for relation in relations:
            print(f"ID: {relation.theme_adviser_group_id}, ID Темы: {relation.theme_id}, ID Группы руководителей: {relation.adviser_group_id}")

    def add_init_theme_adviser_group(self):
        session = self.Session()
        themes = session.query(Theme).all()
        adviser_groups = session.query(AdviserGroup).all()

        for theme in themes:
            adviser_group = rnd.choice(adviser_groups)
            self.add_theme_adviser_group(theme.theme_id, adviser_group.adviser_group_id)
        session.close()


class ThemeSubjectImportanceRepository:
    def __init__(self, engine,theme_repository,subject_repository):
        self.Session = sessionmaker(bind=engine)
        self.theme_repository = theme_repository
        self.subject_repository = subject_repository


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
        theme_subject_importance = session.query(ThemeSubjectImportance).filter(
            ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        session.close()
        return theme_subject_importance

    def update_theme_subject_importance(self, theme_subject_importance_id, theme_id=None, subject_id=None, weight=None):
        session = self.Session()
        theme_subject_importance_record = session.query(ThemeSubjectImportance).filter(
            ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        if theme_subject_importance_record:
            if theme_id is not None: theme_subject_importance_record.theme_id = theme_id
            if subject_id is not None: theme_subject_importance_record.subject_id = subject_id
            if weight is not None: theme_subject_importance_record.weight = weight
            session.commit()
        session.close()

    def delete_theme_subject_importance(self, theme_subject_importance_id):
        session = self.Session()
        theme_subject_importance_record = session.query(ThemeSubjectImportance).filter(
            ThemeSubjectImportance.theme_subject_importance_id == theme_subject_importance_id).first()
        if theme_subject_importance_record:
            session.delete(theme_subject_importance_record)
            session.commit()
        session.close()

    def display_all_theme_subject_importances(self):
        theme_subject_importances = self.get_all_theme_subject_importances()
        for importance in theme_subject_importances:
            print(
                f"ID: {importance.theme_subject_importance_id}, ID Темы: {importance.theme_id}, ID Предмета: "
                f"{importance.subject_id}, Вес: {round(importance.weight, 2)}")

    def add_random_importances_for_themes(self, themes, subjects, min_count=3, max_count=5):
        session = self.Session()
        try:
            for theme in themes:
                subject_count = rnd.randint(min_count, max_count)
                selected_subjects = rnd.sample(subjects, subject_count)

                for subject in selected_subjects:
                    weight = rnd.uniform(0.1, 1.0)
                    self.add_theme_subject_importance(theme.theme_id, subject.subject_id, weight)
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

    def delete_all_theme_subject_importances(self):
        session = self.Session()
        try:
            session.query(ThemeSubjectImportance).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


class StudentSubjectGradeRepository:
    def __init__(self, engine,student_repository, subject_repository):
        self.Session = sessionmaker(bind=engine)
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    def add_student_subject_grade(self, student_id, subject_id, grade):
        session = self.Session()
        new_student_subject_grade = StudentSubjectGrade(student_id=student_id, subject_id=subject_id, grade=grade)
        session.add(new_student_subject_grade)
        session.commit()
        session.close()

    def get_all_student_subject_grades(self):
        session = self.Session()
        student_subject_grades = session.query(StudentSubjectGrade).all()
        session.close()
        return student_subject_grades

    def get_student_subject_grade_by_id(self, student_subject_grade_id):
        session = self.Session()
        student_subject_grade = session.query(StudentSubjectGrade).filter(
            StudentSubjectGrade.student_subject_grade_id == student_subject_grade_id).first()
        session.close()
        return student_subject_grade

    def update_student_subject_grade(self, student_subject_grade_id, student_id=None, subject_id=None, grade=None):
        session = self.Session()
        student_subject_grade_record = session.query(StudentSubjectGrade).filter(
            StudentSubjectGrade.student_subject_grade_id == student_subject_grade_id).first()
        if student_subject_grade_record:
            if student_id is not None: student_subject_grade_record.student_id = student_id
            if subject_id is not None: student_subject_grade_record.subject_id = subject_id
            if grade is not None: student_subject_grade_record.grade = grade
            session.commit()
        session.close()

    def delete_student_subject_grade(self, student_subject_grade_id):
        session = self.Session()
        student_subject_grade_record = session.query(StudentSubjectGrade).filter(
            StudentSubjectGrade.student_subject_id == student_subject_grade_id).first()
        if student_subject_grade_record:
            session.delete(student_subject_grade_record)
            session.commit()
        session.close()

    def display_all_student_subject_grades(self):
        student_subject_grades = self.get_all_student_subject_grades()
        for grade in student_subject_grades:
            print(
                f"ID: {grade.student_subject_grade_id}, ID Студента: {grade.student_id}, ID Предмета: {grade.subject_id}, "
                f"Оценка: {grade.grade}")

    def delete_all_student_subject_grades(self):
        session = self.Session()
        try:
            session.query(StudentSubjectGrade).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


class StudentThemeInterestRepository:
    def __init__(self, engine, student_repository, theme_repository):
        self.Session = sessionmaker(bind=engine)
        self.student_repository = student_repository
        self.theme_repository = theme_repository

    def add_student_theme_interest(self, student_id, theme_id, interest_level):
        session = self.Session()
        new_student_theme_interest = StudentThemeInterest(student_id=student_id, theme_id=theme_id, interest_level=interest_level)
        session.add(new_student_theme_interest)
        session.commit()
        session.close()

    def add_multiple_student_theme_interests(self, student_id, interests):
        session = self.Session()
        try:
            for theme_id, interest_level in interests:
                self.add_student_theme_interest(student_id, theme_id, interest_level)
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении интересов: {e}")
        finally:
            session.close()

    @staticmethod
    def generate_random_interests():
        interest_levels = [1, 2, 3, 4, 5]
        rnd.shuffle(interest_levels)
        interests = [(theme_id, level) for theme_id, level in zip(range(1, 5), interest_levels[:4])]
        return interests

    def initialize_student_interests(self):
        students = self.student_repository.get_all_students()  # Получаем всех студентов

        for student in students:
            interests = self.generate_random_interests()  # Генерируем случайные интересы
            self.add_multiple_student_theme_interests(student.student_id, interests)

    def get_all_student_theme_interests(self):
        session = self.Session()
        student_theme_interests = session.query(StudentThemeInterest).all()
        session.close()
        return student_theme_interests

    def get_student_theme_interest_by_id(self, student_theme_interest_id):
        session = self.Session()
        student_theme_interest = session.query(StudentThemeInterest).filter(
            StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        session.close()
        return student_theme_interest

    def update_student_theme_interest(self, student_theme_interest_id, student_id=None, theme_id=None, interest_level=None):
        session = self.Session()
        student_theme_interest_record = session.query(StudentThemeInterest).filter(
            StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        if student_theme_interest_record:
            if student_id is not None: student_theme_interest_record.student_id = student_id
            if theme_id is not None: student_theme_interest_record.theme_id = theme_id
            if interest_level is not None: student_theme_interest_record.interest_level = interest_level
            session.commit()
        session.close()

    def delete_student_theme_interest(self, student_theme_interest_id):
        session = self.Session()
        student_theme_interest_record = session.query(StudentThemeInterest).filter(
            StudentThemeInterest.student_theme_interest_id == student_theme_interest_id).first()
        if student_theme_interest_record:
            session.delete(student_theme_interest_record)
            session.commit()
        session.close()

    def display_all_student_theme_interests(self):
        student_theme_interests = self.get_all_student_theme_interests()
        for interest in student_theme_interests:
            print(
                f"ID: {interest.student_theme_interest_id}, ID Студента: {interest.student_id}, "
                f"ID Темы: {interest.theme_id}, Уровень интереса: {interest.interest_level}")

    def delete_all_student_theme_interests(self):
        session = self.Session()
        try:
            session.query(StudentThemeInterest).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


class DistributionRepository:
    def __init__(self, engine, student_subject_grade_repo, student_theme_interest_repo, theme_subject_importance_repo, theme_adviser_group_repo):
        self.engine = engine
        self.student_grade_record_repo = student_subject_grade_repo
        self.student_theme_interest_repo = student_theme_interest_repo
        self.theme_subject_importance_repo = theme_subject_importance_repo
        self.theme_adviser_group_repo = theme_adviser_group_repo
        self.Session = sessionmaker(bind=self.engine)

    def add_distribution(self, theme_subject_importance_id, student_subject_grade_id, student_theme_interest_id, theme_adviser_group_id):
        session = self.Session()
        try:
            new_distribution = Distribution(
                theme_subject_importance_id=theme_subject_importance_id,
                student_subject_grade_id=student_subject_grade_id,
                student_theme_interest_id=student_theme_interest_id,
                theme_adviser_group_id=theme_adviser_group_id
            )
            session.add(new_distribution)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении распределения: {e}")
        finally:
            session.close()

    def get_all_distributions(self):
        session = self.Session()
        try:
            distributions = session.query(Distribution).all()
            return distributions
        finally:
            session.close()

    def get_distribution_by_id(self, distribution_id):
        session = self.Session()
        try:
            distribution = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            return distribution
        finally:
            session.close()

    def update_distribution(self, distribution_id, theme_subject_importance_id=None, student_subject_grade_id=None,
                            student_theme_interest_id=None, theme_adviser_group_id=None):  # Добавлен параметр
        session = self.Session()
        try:
            distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            if distribution_record:
                if theme_subject_importance_id is not None:
                    distribution_record.theme_subject_importance_id = theme_subject_importance_id
                if student_subject_grade_id is not None:
                    distribution_record.student_subject_grade_id = student_subject_grade_id
                if student_theme_interest_id is not None:
                    distribution_record.student_theme_interest_id = student_theme_interest_id
                if theme_adviser_group_id is not None:  # Обновление группы советников
                    distribution_record.theme_adviser_group_id = theme_adviser_group_id
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении распределения: {e}")
        finally:
            session.close()

    def delete_distribution(self, distribution_id):
        session = self.Session()
        try:
            distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            if distribution_record:
                session.delete(distribution_record)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении распределения: {e}")
        finally:
            session.close()

    def delete_all_distributions(self):
        session = self.Session()
        try:
            session.query(Distribution).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

    def display_all_distributions(self):
        distributions = self.get_all_distributions()
        for distribution in distributions:
            print(
                f"ID: {distribution.distribution_id}, "
                f"ID Важности Темы и Предмета: {distribution.theme_subject_importance_id}, "
                f"ID Оценки Студента: {distribution.student_subject_grade_id}, "
                f"ID Интереса Студента: {distribution.student_theme_interest_id}, "
                f"ID Группы Советников: {distribution.theme_adviser_group_id}"  # Добавлено отображение группы советников
            )

    def link_theme_subject_importance_with_student_subject_grade(self):
        session = self.Session()
        importance_sum = {}
        try:
            theme_subject_importance_records = session.query(ThemeSubjectImportance).all()
            student_subject_grade_records = session.query(StudentSubjectGrade).all()

            for theme_importance in theme_subject_importance_records:
                theme_id = theme_importance.theme_id
                subject_id = theme_importance.subject_id
                weight = theme_importance.weight

                for grade_record in student_subject_grade_records:
                    if grade_record.subject_id == subject_id:
                        student_id = grade_record.student_id
                        grade = grade_record.grade

                        weighted_grade = grade * weight

                        if (theme_id, student_id) not in importance_sum:
                            importance_sum[(theme_id, student_id)] = 0
                        importance_sum[(theme_id, student_id)] += weighted_grade
        finally:
            session.close()
        return importance_sum

    def link_weighted_grades_with_interest(self):
        session = self.Session()
        result = []
        try:
            # Получаем суммы взвешенных оценок
            importance_sums = self.link_theme_subject_importance_with_student_subject_grade()

            # Получаем интерес студентов к темам
            student_theme_interests = session.query(StudentThemeInterest).all()

            for (theme_id, student_id), total_weighted_grade in importance_sums.items():
                # Ищем уровень интереса студента к теме
                interest_level = next((interest.interest_level for interest in student_theme_interests
                                       if interest.student_id == student_id and interest.theme_id == theme_id), None)
                if interest_level is not None:
                    result.append((theme_id, student_id, total_weighted_grade, interest_level))

        finally:
            session.close()
        return result

    def assign_students_to_advisers(self, sorted_results):
        session = self.Session()
        unassigned_students = []

        try:
            # Получаем все группы советников
            adviser_groups = {group.adviser_group_id: group for group in session.query(AdviserGroup).all()}
            advisers = {adviser.adviser_id: adviser for adviser in session.query(Adviser).all()}

            print("Назначение студентов советникам:")

            for theme_id, student_id, total_weighted_grade, interest_level in sorted_results:
                # Получаем группу советников для темы
                theme_adviser_group = self.theme_adviser_group_repo.get_adviser_group_by_theme(theme_id)
                if theme_adviser_group:
                    adviser_group_id = theme_adviser_group.adviser_group_id
                    # Находим доступных советников из этой группы
                    available_advisers = [
                        adviser for adviser in advisers.values()
                        if adviser.adviser_group_id == adviser_group_id and
                           adviser.number_of_places > 0
                    ]

                    if available_advisers:
                        adviser = available_advisers[0]
                        self.add_distribution(
                            theme_subject_importance_id=theme_id,
                            student_subject_grade_id=student_id,
                            student_theme_interest_id=interest_level,
                            theme_adviser_group_id=adviser_group_id
                        )
                        adviser.number_of_places -= 1
                        print(
                            f"Студент ID: {student_id} назначен к советнику ID : {adviser.adviser_id} по теме ID: {theme_id}, Группа советников ID: {adviser_group_id}"
                        )
                    else:
                        unassigned_students.append(student_id)

        except Exception as e:
            session.rollback()
            print(f"Ошибка при назначении студентов: {e}")
        finally:
            session.close()

        return unassigned_students

    def distribution_algorithm(self):
        student_subject_grades = self.student_grade_record_repo.get_all_student_subject_grades()

        # Вывод всех оценок студентов
        for grade_record in student_subject_grades:
            print(
                f"Студент ID: {grade_record.student_id}, Предмет ID: {grade_record.subject_id}, Оценка: {grade_record.grade}"
            )

        # Получаем суммы взвешенных оценок и уровень интереса
        weighted_grades_with_interest = self.link_weighted_grades_with_interest()

        # Сортируем по убыванию суммы взвешенных оценок, затем по убыванию уровня интереса
        sorted_results = sorted(weighted_grades_with_interest, key=lambda x: (-x[2], x[3]))

        print("\nРезультаты сортировки студентов по сумме взвешенных оценок и уровню интереса:")
        for theme_id, student_id, total_weighted_grade, interest_level in sorted_results:
            print(
                f"Тема ID: {theme_id}, Студент ID: {student_id}, Сумма взвешенных оценок: {round(total_weighted_grade, 2)}, Уровень интереса: {interest_level}"
            )

        # Теперь вызываем метод для назначения студентов советникам
        unassigned_students = self.assign_students_to_advisers(sorted_results)

        # Дополнительная информация о нераспределенных студентах
        if unassigned_students:
            print("Некоторые студенты не были распределены:")
            for student_id in unassigned_students:
                print(f"Студент ID: {student_id}")
        else:
            print("Все студенты успешно распределены к советникам.")