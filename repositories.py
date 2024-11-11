from sqlalchemy.orm import sessionmaker
from models import (Student, Adviser, Subject, Theme,
                    ThemeSubjectImportance, StudentSubjectGrade, StudentThemeInterest, Distribution)
from faker import Faker
import random as rnd

fake = Faker('ru_RU')

class BaseRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def get_all(self, model):
        session = self.Session()
        try:
            return session.query(model).all()
        finally:
            session.close()

    def get_by_id(self, model, record_id):
        session = self.Session()
        try:
            return session.query(model).filter(model.id == record_id).first()
        finally:
            session.close()

    def delete_all(self, model):
        session = self.Session()
        try:
            session.query(model).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

class StudentRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_student(self, firstname, lastname, patronymic, group_student):
        session = self.Session()
        new_student = Student(firstname=firstname, lastname=lastname, patronymic=patronymic, group_student=group_student)
        session.add(new_student)
        session.commit()
        session.close()

    def update_student(self, student_id, firstname=None, lastname=None, patronymic=None, group_student=None):
        session = self.Session()
        student = self.get_by_id(Student, student_id)
        if student:
            if firstname: student.firstname = firstname
            if lastname: student.lastname = lastname
            if patronymic: student.patronymic = patronymic
            if group_student: student.group_student = group_student
            session.commit()
        session.close()

    def delete_student(self, student_id):
        session = self.Session()
        student = self.get_by_id(Student, student_id)
        if student:
            session.delete(student)
            session.commit()
        session.close()

    def add_initial_students(self, count=10):
        for _ in range(count):
            self.add_student(fake.first_name_male(), fake.last_name_male(), fake.first_name_male(),
                             f"A-{fake.random_int(1, 3)}-21")

    def display_all_students(self):
        students = self.get_all(Student)
        for student in students:
            print(
                f"ID Студента: {student.student_id}, Имя: {student.firstname} {student.lastname}, "
                f"Группа: {student.group_student}")
6

class AdviserRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_adviser(self, firstname, lastname, patronymic, number_of_places):
        session = self.Session()
        new_adviser = Adviser(firstname=firstname, lastname=lastname, patronymic=patronymic, number_of_places=number_of_places)
        session.add(new_adviser)
        session.commit()
        session.close()

    def update_adviser(self, adviser_id, firstname=None, lastname=None, patronymic=None, number_of_places=None):
        session = self.Session()
        adviser_record = self.get_by_id(Adviser, adviser_id)
        if adviser_record:
            if firstname: adviser_record.firstname = firstname
            if lastname: adviser_record.lastname = lastname
            if patronymic: adviser_record.patronymic = patronymic
            if number_of_places is not None: adviser_record.number_of_places = number_of_places
            session.commit()
        session.close()

    def delete_adviser(self, adviser_id):
        session = self.Session()
        adviser_record = self.get_by_id(Adviser, adviser_id)
        if adviser_record:
            session.delete(adviser_record)
            session.commit()
        session.close()

    def add_initial_advisers(self, count=5):
        for _ in range(count):
            self.add_adviser(fake.first_name_male(), fake.last_name_male(), fake.first_name_male(),
                             fake.random_int(min=1, max=2))

    def display_all_advisers(self):
        advisers = self.get_all(Adviser)
        for adviser in advisers:
            print(
                f"ID Руководителя: {adviser.adviser_id}, Имя: {adviser.firstname} {adviser.lastname}, Мест: "
                f"{adviser.number_of_places}")


class SubjectRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_subject(self, subject_name):
        session = self.Session()
        new_subject = Subject(subject_name=subject_name)
        session.add(new_subject)
        session.commit()
        session.close()

    def update_subject(self, subject_id, subject_name):
        session = self.Session()
        subject = self.get_by_id(Subject, subject_id)
        if subject:
            subject.subject_name = subject_name
            session.commit()
        session.close()

    def delete_subject(self, subject_id):
        session = self.Session()
        subject = self.get_by_id(Subject, subject_id)
        if subject:
            session.delete(subject)
            session.commit()
        session.close()

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
            self.add_subject(rnd.choice(subjects_list))

    def display_all_subjects(self):
        subjects = self.get_all(Subject)
        for subject in subjects:
            print(f"ID Предмета: {subject.subject_id}, Название: {subject.subject_name}")


class ThemeRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_theme(self, theme_name):
        session = self.Session()
        new_theme = Theme(theme_name=theme_name)
        session.add(new_theme)
        session.commit()
        session.close()

    def update_theme(self, theme_id, theme_name=None):
        session = self.Session()
        theme_record = self.get_by_id(Theme, theme_id)
        if theme_record:
            if theme_name: theme_record.theme_name = theme_name
            session.commit()
        session.close()

    def delete_theme(self, theme_id):
        session = self.Session()
        theme_record = self.get_by_id(Theme, theme_id)
        if theme_record:
            session.delete(theme_record)
            session.commit()
        session.close()

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
            self.add_theme(rnd.choice(themes))

    def display_all_themes(self):
        themes = self.get_all(Theme)
        for theme in themes:
            print(f"ID Темы: {theme.theme_id}, Название: {theme.theme_name}")


# class AdviserGroupRepository(BaseRepository):
#     def __init__(self, engine, adviser_repository):
#         super().__init__(engine)
#         self.adviser_repository = adviser_repository
#
#     def add_adviser_in_group(self, adviser_id, group_specialization):
#         session = self.Session()
#         new_adviser_group = AdviserGroup(adviser_id=adviser_id, group_specialization=group_specialization)
#         session.add(new_adviser_group)
#         session.commit()
#         session.close()
#
#     def update_adviser_group(self, adviser_group_id, adviser_id=None, specialization=None):
#         session = self.Session()
#         adviser_group_record = self.get_by_id(AdviserGroup, adviser_group_id)
#         if adviser_group_record:
#             if adviser_id is not None: adviser_group_record.adviser_id = adviser_id
#             if specialization: adviser_group_record.group_specialization = specialization
#             session.commit()
#         session.close()
#
#     def delete_adviser_group(self, adviser_group_id):
#         session = self.Session()
#         adviser_group_record = self.get_by_id(AdviserGroup, adviser_group_id)
#         if adviser_group_record:
#             session.delete(adviser_group_record)
#             session.commit()
#         session.close()
#
#     def display_all_adviser_groups(self):
#         adviser_groups = self.get_all(AdviserGroup)
#         for group in adviser_groups:
#             print(
#                 f"ID Группы руководителей: {group.adviser_group_id}, ID Руководителя: {group.adviser_id}, "
#                 f"Специализация: {group .group_specialization}")
#
#     def init_all_adviser_groups(self, advisers):
#         group_specializations = ["Специализация 1", "Специализация 2"]
#         for adviser in advisers:
#             specialization = rnd.choice(group_specializations)
#             self.add_adviser_in_group(adviser.adviser_id, specialization)
#

class ThemeSubjectImportanceRepository(BaseRepository):
    def __init__(self, engine, theme_repository, subject_repository):
        super().__init__(engine)
        self.theme_repository = theme_repository
        self.subject_repository = subject_repository

    def add_theme_subject_importance(self, theme_id, subject_id, weight):
        session = self.Session()
        new_theme_subject_importance = ThemeSubjectImportance(theme_id=theme_id, subject_id=subject_id, weight=weight)
        session.add(new_theme_subject_importance)
        session.commit()
        session.close()

    def update_theme_subject_importance(self, theme_subject_importance_id, theme_id=None, subject_id=None, weight=None):
        session = self.Session()
        theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance, theme_subject_importance_id)
        if theme_subject_importance_record:
            if theme_id is not None: theme_subject_importance_record.theme_id = theme_id
            if subject_id is not None: theme_subject_importance_record.subject_id = subject_id
            if weight is not None: theme_subject_importance_record.weight = weight
            session.commit()
        session.close()

    def delete_theme_subject_importance(self, theme_subject_importance_id):
        session = self.Session()
        theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance, theme_subject_importance_id)
        if theme_subject_importance_record:
            session.delete(theme_subject_importance_record)
            session.commit()
        session.close()

    def display_all_theme_subject_importances(self):
        theme_subject_importances = self.get_all(ThemeSubjectImportance)
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

                # Генерируем случайные веса
                weights = [rnd.uniform(0.1, 1.0) for _ in selected_subjects]
                total_weight = sum(weights)

                # Нормализуем веса
                normalized_weights = [weight / total_weight for weight in weights]

                # Проверка на сумму весов
                assert abs(sum(normalized_weights) - 1.0) < 1e-6, "Сумма нормализованных весов не равна 1"

                for subject, normalized_weight in zip(selected_subjects, normalized_weights):
                    self.add_theme_subject_importance(theme.theme_id, subject.subject_id, normalized_weight)
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

class StudentSubjectGradeRepository(BaseRepository):
    def __init__(self, engine, student_repository, subject_repository):
        super().__init__(engine)
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    def add_student_subject_grade(self, student_id, subject_id, grade):
        session = self.Session()
        new_student_subject_grade = StudentSubjectGrade(student_id=student_id, subject_id=subject_id, grade=grade)
        session.add(new_student_subject_grade)
        session.commit()
        session.close()

    def update_student_subject_grade(self, student_subject_grade_id, student_id=None, subject_id=None, grade=None):
        session = self.Session()
        student_subject_grade_record = self.get_by_id(StudentSubjectGrade, student_subject_grade_id)
        if student_subject_grade_record:
            if student_id is not None: student_subject_grade_record.student_id = student_id
            if subject_id is not None: student_subject_grade_record.subject_id = subject_id
            if grade is not None: student_subject_grade_record.grade = grade
            session.commit()
        session.close()

    def delete_student_subject_grade(self, student_subject_grade_id):
        session = self.Session()
        student_subject_grade_record = self.get_by_id(StudentSubjectGrade, student_subject_grade_id)
        if student_subject_grade_record:
            session.delete(student_subject_grade_record)
            session.commit()
        session.close()


    def display_all_student_subject_grades(self):
        student_subject_grades = self.get_all(StudentSubjectGrade)
        for grade in student_subject_grades:
            print(
                f"ID: {grade.student_subject_grade_id}, ID Студента: {grade.student_id}, ID Предмета: {grade.subject_id}, "
                f"Оценка: {grade.grade}")


class StudentThemeInterestRepository(BaseRepository):
    def __init__(self, engine, student_repository, theme_repository):
        super().__init__(engine)
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
        students = self.student_repository.get_all(Student)  # Исправлено на get_all(Student)
        for student in students:
            interests = self.generate_random_interests()
            self.add_multiple_student_theme_interests(student.student_id, interests)

    def display_all_student_theme_interests(self):
        student_theme_interests = self.get_all(StudentThemeInterest)
        for interest in student_theme_interests:
            print(
                f"ID: {interest.student_theme_interest_id}, ID Студента: {interest.student_id}, "
                f"ID Темы: {interest.theme_id}, Уровень интереса: {interest.interest_level}")


class DistributionRepository:
    def __init__(self, engine, student_subject_grade_repo, student_theme_interest_repo, theme_subject_importance_repo):
        self.engine = engine
        self.student_grade_record_repo = student_subject_grade_repo
        self.student_theme_interest_repo = student_theme_interest_repo
        self.theme_subject_importance_repo = theme_subject_importance_repo
        self.Session = sessionmaker(bind=self.engine)

    def add_distribution(self, theme_subject_importance_id, student_subject_grade_id, student_theme_interest_id):
        session = self.Session()
        try:
            new_distribution = Distribution(
                theme_subject_importance_id=theme_subject_importance_id,
                student_subject_grade_id=student_subject_grade_id,
                student_theme_interest_id=student_theme_interest_id,
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

    def update_distribution(self, distribution_id, theme_subject_importance_id=None, student_subject_grade_id=None,
                            student_theme_interest_id=None):
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
            session.close 
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

    def link_theme_subject_importance_with_student_subject_grade(self):
        session = self.Session()
        suitability_scores = {}
        try:
            theme_subject_importance_records = session.query(ThemeSubjectImportance).all()
            student_subject_grade_records = session.query(StudentSubjectGrade).all()

            subject_weights = {}
            for importance in theme_subject_importance_records:
                theme_id = importance.theme_id
                subject_id = importance.subject_id
                weight = importance.weight

                if theme_id not in subject_weights:
                    subject_weights[theme_id] = {}
                subject_weights[theme_id][subject_id] = weight

            for theme_id, subjects in subject_weights.items():
                for subject_id, weight in subjects.items():
                    for grade_record in student_subject_grade_records:
                        if grade_record.subject_id == subject_id:
                            student_id = grade_record.student_id
                            grade = grade_record.grade

                            weighted_grade = grade * weight

                            if (theme_id, student_id) not in suitability_scores:
                                suitability_scores[(theme_id, student_id)] = 0

                            suitability_scores[(theme_id, student_id)] += weighted_grade

            for key in suitability_scores:
                max_possible_score = sum(weight * 5 for weight in subject_weights[key[0]].values())
                suitability_scores[key] = (suitability_scores[key] / max_possible_score) * 100

        finally:
            session.close()
        return suitability_scores

    def link_weighted_grades_with_interest(self):
        session = self.Session()
        result = []
        try:
            suitability_scores = self.link_theme_subject_importance_with_student_subject_grade()
            student_theme_interests = session.query(StudentThemeInterest).all()

            for (theme_id, student_id), suitability_score in suitability_scores.items():
                interest_level = next((interest.interest_level for interest in student_theme_interests
                                       if interest.student_id == student_id and interest.theme_id == theme_id), None)
                if interest_level is not None:
                    result.append((theme_id, student_id, suitability_score, interest_level))

        finally:
            session.close()
        return result

    def assign_students_to_advisers(self, sorted_results):
        session = self.Session()
        unassigned_students = set()
        assigned_students = set()
        assigned_themes = set()

        try:
            advisers = {adviser.adviser_id: adviser for adviser in session.query(Adviser).all()}

            print("Назначение студентов преподавателям:")

            for theme_id, student_id, total_weighted_grade, interest_level in sorted_results:
                if student_id in assigned_students:
                    continue

                if theme_id in assigned_themes:
                    continue

                available_advisers = [
                    adviser for adviser in advisers.values()
                    if adviser.number_of_places > 0
                ]

                if available_advisers:
                    adviser = available_advisers[0]
                    self.add_distribution(
                        theme_subject_importance_id=theme_id,
                        student_subject_grade_id=student_id,
                        student_theme_interest_id=interest_level,
                    )
                    adviser.number_of_places -= 1
                    print(
                        f"Студент ID: {student_id} назначен к преподавателю ID : {adviser.adviser_id} по теме ID: {theme_id}"
                    )
                    assigned_students.add(student_id)
                    assigned_themes.add(theme_id)
                else:
                    unassigned_students.add(student_id)

        except Exception as e:
            session.rollback()
            print(f"Ошибка при назначении студентов: {e}")
        finally:
            session.close()

        return sorted(unassigned_students)

    def distribution_algorithm(self):
        suitability_results = self.link_weighted_grades_with_interest()
        sorted_results = sorted(suitability_results, key=lambda x: (x[3], -x[2], x[0]))

        print("\nРезультаты сортировки студентов по уровню интереса и степени подходимости :")
        for theme_id, student_id, suitability_score, interest_level in sorted_results:
            print(
                f"Тема ID: {theme_id}, Студент ID: {student_id}, Степень подходимости: {round(suitability_score, 2)}%, "
                f"Уровень интереса: {interest_level}"
            )

        unassigned_students = self.assign_students_to_advisers(sorted_results)

        if unassigned_students:
            print("Некоторые студенты не были распределены:")
            for student_id in unassigned_students:
                print(f"Студент ID: {student_id}")
        else:
            print("Все студенты успешно распределены к научным руководителям.")