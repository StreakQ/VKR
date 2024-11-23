from sqlalchemy.orm import sessionmaker
from models import (Student, Adviser, Subject, Theme,
                    ThemeSubjectImportance, StudentSubjectGrade, StudentThemeInterest, Distribution, AdviserTheme, DistributionAlgorithm)
from faker import Faker
import random as rnd
import logging

fake = Faker('ru_RU')

class BaseRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def get_all(self, model):
        with self.Session() as session:
            return session.query(model).all()

    def get_by_id(self, model, record_id):
        with self.Session() as session:
            return session.query(model).filter(model.id == record_id).first()

    def delete_all(self, model):
        with self.Session() as session:
            try:
                session.query(model).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)


class StudentRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_student(self, firstname, lastname, patronymic, group_student):
        with self.Session() as session:
            new_student = Student(firstname=firstname, lastname=lastname, patronymic=patronymic, group_student=group_student)
            session.add(new_student)
            session.commit()

    def update_student(self, student_id, firstname=None, lastname=None, patronymic=None, group_student=None):
        with self.Session() as session:
            student = self.get_by_id(Student, student_id)
            if student:
                if firstname: student.firstname = firstname
                if lastname: student.lastname = lastname
                if patronymic: student.patronymic = patronymic
                if group_student: student.group_student = group_student
                session.commit()

    def delete_student(self, student_id):
        with self.Session() as session:
            student = self.get_by_id(Student, student_id)
            if student:
                session.delete(student)
                session.commit()

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


class AdviserRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_adviser(self, firstname, lastname, patronymic, number_of_places):
        with self.Session() as session:
            new_adviser = Adviser(firstname=firstname, lastname=lastname, patronymic=patronymic, number_of_places=number_of_places)
            session.add(new_adviser)
            session.commit()

    def update_adviser(self, adviser_id, firstname=None, lastname=None, patronymic=None, number_of_places=None):
        with self.Session() as session:
            adviser_record = self.get_by_id(Adviser, adviser_id)
            if adviser_record:
                if firstname: adviser_record.firstname = firstname
                if lastname: adviser_record.lastname = lastname
                if patronymic: adviser_record.patronymic = patronymic
                if number_of_places is not None: adviser_record.number_of_places = number_of_places
                session.commit()

    def delete_adviser(self, adviser_id):
        with self.Session() as session:
            adviser_record = self.get_by_id(Adviser, adviser_id)
            if adviser_record:
                session.delete(adviser_record)
                session.commit()

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
        with self.Session() as session:
            new_subject = Subject(subject_name=subject_name)
            session.add(new_subject)
            session.commit()

    def update_subject(self, subject_id, subject_name):
        with self.Session() as session:
            subject = self.get_by_id(Subject, subject_id)
            if subject:
                subject.subject_name = subject_name
                session.commit()

    def delete_subject(self, subject_id):
        with self.Session() as session:
            subject = self.get_by_id(Subject, subject_id)
            if subject:
                session.delete(subject)
                session.commit()

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
        with self.Session() as session:
            new_theme = Theme(theme_name=theme_name)
            session.add(new_theme)
            session.commit()

    def update_theme(self, theme_id, theme_name=None):
        with self.Session() as session:
            theme_record = self.get_by_id(Theme, theme_id)
            if theme_record:
                if theme_name: theme_record.theme_name = theme_name
                session.commit()

    def delete_theme(self, theme_id):
        with self.Session() as session:
            theme_record = self.get_by_id(Theme, theme_id)
            if theme_record:
                session.delete(theme_record)
                session.commit()

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


class AdviserThemeRepository(BaseRepository):
    def __init__(self, engine, adviser_repository, theme_repository):
        super().__init__(engine)
        self.adviser_repository = adviser_repository
        self.theme_repository = theme_repository


    def add_adviser_theme_priority(self, adviser_id, theme_id, priority_level):
        with self.Session() as session:
            new_adviser_theme_priority = AdviserTheme(adviser_id=adviser_id, theme_id=theme_id, priority=priority_level)
            session.add(new_adviser_theme_priority)
            session.commit()

    def delete_adviser_theme_priority(self, adviser_id, theme_id, priority_level):
        with self.Session() as session:
            delete_adviser_theme_priority = session.query(AdviserTheme).filter(
                AdviserTheme.adviser_id == adviser_id,
                AdviserTheme.theme_id == theme_id,
                AdviserTheme.priority == priority_level
            ).first()
            if delete_adviser_theme_priority:
                session.delete(delete_adviser_theme_priority)
                session.commit()

    def display_all_adviser_theme_priorities(self):
        adviser_theme_priorities = self.get_all(AdviserTheme)
        for priority in adviser_theme_priorities:
            print(
                f"ID: {priority.adviser_theme_id}, ID Научного руководителя: {priority.adviser_id}, "
                f"ID Темы: {priority.theme_id}, Уровень приоритета: {priority.priority}"
            )

    def init_random_priorities(self):
        with self.Session() as session:
            try:
                advisers = self.adviser_repository.get_all(Adviser)
                themes = self.theme_repository.get_all(Theme)

                for adviser in advisers:
                    for theme in themes:
                        priority_level = rnd.randint(1, len(themes))

                        existing_priority = session.query(AdviserTheme).filter(
                            AdviserTheme.theme_id == theme.theme_id,
                            AdviserTheme.priority == priority_level
                        ).first()

                        if existing_priority is None:
                            self.add_adviser_theme_priority(adviser.adviser_id, theme.theme_id, priority_level)

            except Exception as e:
                print(f"Ошибка при инициализации приоритетов: {e}")


class ThemeSubjectImportanceRepository(BaseRepository):
    def __init__(self, engine, theme_repository, subject_repository):
        super().__init__(engine)
        self.theme_repository = theme_repository
        self.subject_repository = subject_repository

    def add_theme_subject_importance(self, theme_id, subject_id, weight):
        with self.Session() as session:
            new_theme_subject_importance = ThemeSubjectImportance(theme_id=theme_id, subject_id=subject_id, weight=weight)
            session.add(new_theme_subject_importance)
            session.commit()

    def update_theme_subject_importance(self, theme_subject_importance_id, theme_id=None, subject_id=None, weight=None):
        with self.Session() as session:
            theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance, theme_subject_importance_id)
            if theme_subject_importance_record:
                if theme_id is not None: theme_subject_importance_record.theme_id = theme_id
                if subject_id is not None: theme_subject_importance_record.subject_id = subject_id
                if weight is not None: theme_subject_importance_record.weight = weight
                session.commit()

    def delete_theme_subject_importance(self, theme_subject_importance_id):
        with self.Session() as session:
            theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance, theme_subject_importance_id)
            if theme_subject_importance_record:
                session.delete(theme_subject_importance_record)
                session.commit()

    def display_all_theme_subject_importances(self):
        theme_subject_importances = self.get_all(ThemeSubjectImportance)
        for importance in theme_subject_importances:
            print(
                f"ID: {importance.theme_subject_importance_id}, ID Темы: {importance.theme_id}, ID Предмета: "
                f"{importance.subject_id}, Вес: {round(importance.weight, 2)}")

    def add_random_importances_for_themes(self, themes, subjects, min_count=3, max_count=5):
        with self.Session() as session:
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

class StudentSubjectGradeRepository(BaseRepository):
    def __init__(self, engine, student_repository, subject_repository):
        super().__init__(engine)
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    def add_student_subject_grade(self, student_id, subject_id, grade):
        with self.Session() as session:
            new_student_subject_grade = StudentSubjectGrade(student_id=student_id, subject_id=subject_id, grade=grade)
            session.add(new_student_subject_grade)
            session.commit()

    def update_student_subject_grade(self, student_subject_grade_id, student_id=None, subject_id=None, grade=None):
        with self.Session() as session:
            student_subject_grade_record = self.get_by_id(StudentSubjectGrade, student_subject_grade_id)
            if student_subject_grade_record:
                if student_id is not None: student_subject_grade_record.student_id = student_id
                if subject_id is not None: student_subject_grade_record.subject_id = subject_id
                if grade is not None: student_subject_grade_record.grade = grade
                session.commit()

    def delete_student_subject_grade(self, student_subject_grade_id):
        with self.Session() as session:
            student_subject_grade_record = self.get_by_id(StudentSubjectGrade, student_subject_grade_id)
            if student_subject_grade_record:
                session.delete(student_subject_grade_record)
                session.commit()

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
        with self.Session() as session:
            new_student_theme_interest = StudentThemeInterest(student_id=student_id, theme_id=theme_id, interest_level=interest_level)
            session.add(new_student_theme_interest)
            session.commit()

    def add_multiple_student_theme_interests(self, student_id, interests):
        with self.Session() as session:
            try:
                for theme_id, interest_level in interests:
                    self.add_student_theme_interest(student_id, theme_id, interest_level)
            except Exception as e:
                session.rollback()
                print(f"Ошибка при добавлении интересов: {e}")

    @staticmethod
    def generate_random_interests():
        interest_levels = [1, 2, 3, 4, 5]
        rnd.shuffle(interest_levels)
        interests = [(theme_id, level) for theme_id, level in zip(range(1, 5), interest_levels[:4])]
        return interests

    def initialize_student_interests(self):
        students = self.student_repository.get_all(Student)
        for student in students:
            interests = self.generate_random_interests()
            self.add_multiple_student_theme_interests(student.student_id, interests)

    def display_all_student_theme_interests(self):
        student_theme_interests = self.get_all(StudentThemeInterest)
        for interest in student_theme_interests:
            print(
                f"ID: {interest.student_theme_interest_id}, ID Студента: {interest.student_id}, "
                f"ID Темы: {interest.theme_id}, Уровень интереса: {interest.interest_level}")


class DistributionAlgorithmRepository(BaseRepository):
    def __init__(self,engine, student_subject_grade_repository, student_theme_interest_repository,
                 theme_subject_importance_repository, adviser_theme_repository):
        super().__init__(engine)
        self.student_grade_record_repository = student_subject_grade_repository
        self.student_theme_interest_repository = student_theme_interest_repository
        self.theme_subject_importance_repository = theme_subject_importance_repository
        self.adviser_theme_repository = adviser_theme_repository

    def create_distribution_algorithm(self):
        with self.Session() as session:
            new_algorithm = DistributionAlgorithm()
            session.add(new_algorithm)
            session.commit()
            return new_algorithm.distribution_algorithm_id

    def link_theme_subject_importance_with_student_subject_grade(self):
        suitability_scores = {}
        with self.student_grade_record_repository.Session() as session:
            theme_subject_importance_records = session.query(ThemeSubjectImportance).all()
            student_subject_grade_records = session.query(StudentSubjectGrade).all()

            print("Темы и важность предметов:")
            for importance in theme_subject_importance_records:
                print(
                    f"Тема ID: {importance.theme_id}, Предмет ID: {importance.subject_id}, Вес: {round(importance.weight, 2)}")

            subject_weights = {}
            for importance in theme_subject_importance_records:
                theme_id = importance.theme_id
                subject_id = importance.subject_id
                weight = importance.weight

                if theme_id not in subject_weights:
                    subject_weights[theme_id] = {}
                subject_weights[theme_id][subject_id] = weight

            print("\nВеса предметов по темам:")
            for theme_id, subjects in subject_weights.items():
                print(
                    f"Тема ID: {theme_id}, Предметы и веса: { {subj_id: round(weight, 2) for subj_id, weight in subjects.items()} }")

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

            print("\nСуммарные взвешенные оценки:")
            for key, score in suitability_scores.items():
                print(f"Тема ID: {key[0]}, Студент ID: {key[1]}, Взвешенная оценка: {round(score, 2)}")

            for key in suitability_scores:
                max_possible_score = sum(weight * 5 for weight in subject_weights[key[0]].values())
                normalized_score = (suitability_scores[key] / max_possible_score) * 100 if max_possible_score > 0 else 0
                suitability_scores[key] = round(normalized_score, 2)

            print("\nНормализованные оценки соответствия:")
            for key, score in suitability_scores.items():
                print(f"Тема ID: {key[0]}, Студент ID: {key[1]}, Степень подходимости студента к теме: {score:.2f}%")

        return suitability_scores

    def link_weighted_grades_with_interest(self):
        result = []
        with self.student_theme_interest_repository.Session() as session:
            suitability_scores = self.link_theme_subject_importance_with_student_subject_grade()
            student_theme_interests = session.query(StudentThemeInterest).all()

            for (theme_id, student_id), suitability_score in suitability_scores.items():
                interest_level = next((interest.interest_level for interest in student_theme_interests
                                       if interest.student_id == student_id and interest.theme_id == theme_id), None)
                if interest_level is not None:
                    result.append((theme_id, student_id, suitability_score, interest_level))

            # Сортировка результатов
            result.sort(key=lambda x: (-x[2], x[3], x[1], x[0]))

            print("\nРезультаты соответствия тем и интересов студентов:")
            for theme_id, student_id, suitability_score, interest_level in result:
                print(f"Студент ID: {student_id}, Тема ID: {theme_id}, "
                      f"Степень подходимости: {round(suitability_score, 2)}%, "
                      f"Уровень интереса: {interest_level}")

        return result

    def assign_students_to_advisers(self, sorted_results):
        unassigned_students = set()
        assigned_students = set()
        assigned_themes = set()
        distributions_to_add = []

        with self.student_theme_interest_repository.Session() as session:
            advisers = {adviser.adviser_id: adviser for adviser in session.query(Adviser).all()}
            adviser_themes = session.query(AdviserTheme).all()

            adviser_priority_dict = {(adviser_theme.adviser_id, adviser_theme.theme_id): adviser_theme.priority
                                     for adviser_theme in adviser_themes}

            for theme_id, student_id, total_weighted_grade, interest_level in sorted_results:
                # Проверяем, был ли студент уже назначен на эту тему
                if student_id in assigned_students:
                    continue
                if theme_id in assigned_themes:
                    continue

                student_interest = session.query(StudentThemeInterest).filter(
                    StudentThemeInterest.student_id == student_id,
                    StudentThemeInterest.theme_id == theme_id
                ).first()

                if not student_interest:
                    continue

                # Находим доступных научных руководителей для данной темы
                available_advisers = [
                    adviser for adviser in advisers.values()
                    if adviser.number_of_places > 0 and any(
                        adviser_theme.theme_id == theme_id for adviser_theme in adviser_themes if
                        adviser_theme.adviser_id == adviser.adviser_id
                    )
                ]

                if available_advisers:
                    available_advisers.sort(
                        key=lambda x: adviser_priority_dict.get((x.adviser_id, theme_id), float('inf'))
                    )

                    adviser = available_advisers[0]
                    adviser_theme_id = next((adviser_theme.theme_id for adviser_theme in adviser_themes if
                                             adviser_theme.adviser_id == adviser.adviser_id), None)

                    # Добавляем распределение
                    distributions_to_add.append({
                        "theme_subject_importance_id": theme_id,
                        "student_subject_grade_id": student_id,
                        "student_theme_interest_id": student_interest.student_theme_interest_id,
                        "adviser_theme_id": adviser_theme_id
                    })
                    adviser.number_of_places -= 1
                    assigned_students.add(student_id)  # Добавляем студента в список назначенных
                    assigned_themes.add(theme_id)  # Добавляем тему в список назначенных
                else:
                    unassigned_students.add(student_id)

        return distributions_to_add, unassigned_students

    def distribution_algorithm(self):
        suitability_results = self.link_weighted_grades_with_interest()
        sorted_results = sorted(suitability_results, key=lambda x: (x[3], -x[2], x[0]))

        distributions_to_add, unassigned_students = self.assign_students_to_advisers(sorted_results)
        return distributions_to_add, unassigned_students


class DistributionRepository(BaseRepository):
    def __init__(self, engine, student_subject_grade_repository, student_theme_interest_repository,
                 theme_subject_importance_repository, adviser_theme_repository, distribution_algorithm_repository):
        super().__init__(engine)
        self.student_grade_record_repository = student_subject_grade_repository
        self.student_theme_interest_repository = student_theme_interest_repository
        self.theme_subject_importance_repository = theme_subject_importance_repository
        self.adviser_theme_repository = adviser_theme_repository
        self.distribution_algorithm_repository = distribution_algorithm_repository

    def add_distribution(self, distributions):
        with self.Session() as session:
            try:
                session.bulk_insert_mappings(Distribution, distributions)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при добавлении распределений: {e}")

    def get_all_distributions(self):
        with self.Session() as session:
            return session.query(Distribution).all()

    def update_distribution(self, distribution_id, theme_subject_importance_id=None, student_subject_grade_id=None,
                            student_theme_interest_id=None, adviser_theme_id=None, distribution_algorithm_id=None):
        with self.Session() as session:
            distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            if distribution_record:
                if theme_subject_importance_id is not None:
                    distribution_record.theme_subject_importance_id = theme_subject_importance_id
                if student_subject_grade_id is not None:
                    distribution_record.student_subject_grade_id = student_subject_grade_id
                if student_theme_interest_id is not None:
                    distribution_record.student_theme_interest_id = student_theme_interest_id
                if adviser_theme_id is not None:
                    distribution_record.adviser_theme_id = adviser_theme_id
                if distribution_algorithm_id is not None:
                    distribution_record.distribution_algorithm_id = distribution_algorithm_id
                session.commit()

    def delete_distribution(self, distribution_id):
        with self.Session() as session:
            distribution_record = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            if distribution_record:
                session.delete(distribution_record)
                session.commit()

    def delete_all_distributions(self):
        with self.Session() as session:
            try:
                session.query(Distribution).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def process_distributions(self, distributions_to_add, distribution_algorithm_id):
        with self.Session() as session:
            try:
                for distribution in distributions_to_add:
                    # Проверяем наличие всех необходимых ключей
                    if not all(key in distribution for key in
                               ["theme_subject_importance_id", "student_subject_grade_id", "student_theme_interest_id",
                                "adviser_theme_id"]):
                        logging.error("Недостаточно данных для распределения: %s", distribution)
                        continue

                    # Проверка на существование распределения для данного студента и темы
                    existing_distribution = session.query(Distribution).filter(
                        Distribution.student_subject_grade_id == distribution["student_subject_grade_id"],
                        Distribution.theme_subject_importance_id == distribution["theme_subject_importance_id"],
                        Distribution.adviser_theme_id == distribution["adviser_theme_id"]
                    ).first()

                    if existing_distribution:
                        logging.warning(
                            f"Распределение уже существует для студента ID {distribution['student_subject_grade_id']} "
                            f"и темы ID {distribution['theme_subject_importance_id']}. Пропускаем.")
                        continue

                    # Создаем новое распределение
                    new_distribution = Distribution(
                        distribution_algorithm_id=distribution_algorithm_id,
                        theme_subject_importance_id=distribution["theme_subject_importance_id"],
                        student_subject_grade_id=distribution["student_subject_grade_id"],
                        student_theme_interest_id=distribution["student_theme_interest_id"],
                        adviser_theme_id=distribution["adviser_theme_id"]
                    )
                    session.add(new_distribution)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.exception("Ошибка при добавлении распределений: %s", e)