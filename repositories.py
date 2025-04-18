
from sqlalchemy.orm import sessionmaker
from models import (Student, Adviser, Subject, Theme,
                    ThemeSubjectImportance, StudentSubjectGrade, StudentThemeInterest, Distribution, AdviserTheme,
                    DistributionAlgorithm)
from faker import Faker
import random as rnd
import logging
from data import *
from collections import defaultdict, deque
import heapq
from werkzeug.security import check_password_hash

fake = Faker('ru_RU')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def get_all(self, model) -> list:
        """Возвращает все записи модели."""
        with self.Session() as session:
            return session.query(model).all()

    def get_by_id(self, model, record_id, id_field: str = "id"):
        """Возвращает запись по ID.
        """
        with self.Session() as session:
            return session.query(model).filter(getattr(model, id_field) == record_id).first()

    def get_id_by_value(self, model, value, column_name: str):
        """
        Возвращает ID записи по значению в указанной колонке.

        :param model: Модель таблицы SQLAlchemy.
        :param value: Значение для поиска.
        :param column_name: Название колонки, по которой выполняется поиск.
        :return: ID записи или None, если запись не найдена.
        """
        with self.Session() as session:
            try:
                # Получаем атрибут модели (колонку) по её имени
                column = getattr(model, column_name)

                # Ищем запись по значению в указанной колонке
                record = session.query(model).filter(column == value).first()

                # Возвращаем ID записи, если она найдена
                return record.id if record else None
            except Exception as e:
                logging.error(f"Ошибка при поиске ID записи: {e}")
                return None

    def delete_all(self, model):
        """Удаляет все записи модели."""
        with self.Session() as session:
            try:
                session.query(model).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при удалении всех записей модели {model.__name__}: {e}")

    def add_record(self, record):
        """Добавляет новую запись."""
        with self.Session() as session:
            try:
                session.add(record)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при добавлении записи: {e}")



    def update_record(self, record, **kwargs):
        """Обновляет запись."""
        with self.Session() as session:
            try:
                for key, value in kwargs.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при обновлении записи: {e}")

    def delete_record(self, record):
        """Удаляет запись."""
        with self.Session() as session:
            try:
                session.delete(record)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при удалении записи: {e}")

    def get_all_filtered(self, model, **filters):
        with self.Session() as session:
            return session.query(model).filter_by(**filters).all()

class StudentRepository(BaseRepository):
    def add_student(self,username:str,password_hash:str, firstname: str, lastname: str, patronymic: str, group_student: str):
        new_student = Student(
            username=username,
            password_hash=password_hash,
            firstname=firstname,
            lastname=lastname,
            patronymic=patronymic,
            group_student=group_student
        )
        self.add_record(new_student)

    def update_student(self, student_id: int, **kwargs):
        student = self.get_by_id(Student, student_id, id_field="student_id")
        if student:
            self.update_record(student, **kwargs)

    def delete_student(self, student_id: int):
        student = self.get_by_id(Student, student_id, id_field="student_id")
        if student:
            self.delete_record(student)

    def add_initial_students(self,logins:list,passwords:list, count: int = 10):
        for i in range(count):
            self.add_student(
                username=logins[i],
                password_hash=passwords[i],
                firstname=fake.first_name_male(),
                lastname=fake.last_name_male(),
                patronymic=fake.first_name_male(),
                group_student=f"A-{fake.random_int(1, 3)}-21"
            )

    def display_all_students(self):
        students = self.get_all(Student)
        for student in students:
            logging.info(
                f"ID Студента: {student.student_id}, "
                f"Имя: {student.firstname} {student.lastname}, "
                f"Группа: {student.group_student}"
            )


class AdviserRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)

    def add_adviser(self, firstname, lastname, patronymic, number_of_places, username, password_hash):
        """
        Добавляет нового научного руководителя в базу данных.
        """
        with self.Session() as session:
            new_adviser = Adviser(
                firstname=firstname,
                lastname=lastname,
                patronymic=patronymic,
                number_of_places=number_of_places,
                username=username,
                password_hash=password_hash
            )
            session.add(new_adviser)
            session.commit()

    def update_adviser(self, adviser_id, firstname=None, lastname=None, patronymic=None, number_of_places=None, username=None, password_hash=None):
        """
        Обновляет данные научного руководителя, включая логин и пароль.
        """
        with self.Session() as session:
            adviser_record = self.get_by_id(Adviser, adviser_id, id_field="adviser_id")
            if adviser_record:
                if firstname:
                    adviser_record.firstname = firstname
                if lastname:
                    adviser_record.lastname = lastname
                if patronymic:
                    adviser_record.patronymic = patronymic
                if number_of_places is not None:
                    adviser_record.number_of_places = number_of_places
                if username:
                    adviser_record.username = username
                if password_hash:
                    adviser_record.password_hash = password_hash
                session.commit()

    def delete_adviser(self, adviser_id):
        """
        Удаляет научного руководителя по ID.
        """
        with self.Session() as session:
            adviser_record = self.get_by_id(Adviser, adviser_id, id_field="adviser_id")
            if adviser_record:
                session.delete(adviser_record)
                session.commit()

    def add_initial_advisers(self, advisers_data):
        """
        Добавляет начальных научных руководителей из предоставленных данных.
        :param advisers_data: Список словарей с данными научных руководителей.
        """
        for adviser in advisers_data:
            self.add_adviser(
                firstname=adviser["firstname"],
                lastname=adviser["lastname"],
                patronymic=adviser["patronymic"],
                number_of_places=adviser["number_of_places"],
                username=adviser["username"],
                password_hash=adviser["password_hash"]
            )

    def display_all_advisers(self):
        """
        Выводит информацию о всех научных руководителях.
        """
        advisers = self.get_all(Adviser)
        for adviser in advisers:
            print(
                f"ID Руководителя: {adviser.adviser_id}, "
                f"Имя: {adviser.firstname} {adviser.lastname} {adviser.patronymic}, "
                f"Логин: {adviser.username}, "
                f"Мест: {adviser.number_of_places}"
            )

    def get_advisers_for_theme(self, theme_id):
        """
        Получает всех научных руководителей, связанных с определенной темой.
        """
        with self.Session() as session:
            return session.query(Adviser).join(AdviserTheme).filter(AdviserTheme.theme_id == theme_id).all()

    def decrease_adviser_places(self, adviser_id, session):
        """
        Уменьшает количество доступных мест у научного руководителя.
        """
        adviser_record = self.get_by_adviser_id(adviser_id, session)
        if adviser_record and adviser_record.number_of_places > 0:
            adviser_record.number_of_places -= 1
            session.commit()

    def increase_adviser_places(self, adviser_id, session):
        """
        Увеличивает количество доступных мест у научного руководителя.
        """
        adviser_record = self.get_by_adviser_id(adviser_id, session)
        if adviser_record:
            adviser_record.number_of_places += 1
            session.commit()

    def get_by_adviser_id(self, adviser_id, session):
        """
        Получает научного руководителя по его ID.
        """
        return session.query(Adviser).filter(Adviser.adviser_id == adviser_id).first()

    def authenticate_adviser(self, username, password):
        """
        Аутентифицирует научного руководителя по логину и паролю.
        """
        with self.Session() as session:
            adviser = session.query(Adviser).filter_by(username=username).first()
            if adviser and check_password_hash(adviser.password_hash, password):
                return adviser
            return None

    def add_adviser_for_app(self, adviser_id, firstname, lastname, patronymic, number_of_places, username, password_hash):
        """
        Добавляет научного руководителя с указанием всех полей.
        """
        with self.Session() as session:
            new_adviser = Adviser(
                adviser_id=adviser_id,
                firstname=firstname,
                lastname=lastname,
                patronymic=patronymic,
                number_of_places=number_of_places,
                username=username,
                password_hash=password_hash
            )
            session.add(new_adviser)
            session.commit()


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
            subject = self.get_by_id(Subject,subject_id, id_field="subject_id")
            if subject:
                subject.subject_name = subject_name
                session.commit()

    def delete_subject(self, subject_id):
        with self.Session() as session:
            subject = self.get_by_id(Subject,subject_id, id_field="subject_id")
            if subject:
                session.delete(subject)
                session.commit()

    def add_initial_subjects(self):
        available_subjects = subjects_data.copy()
        for _ in range(len(available_subjects)):
            selected_subject = rnd.choice(available_subjects)
            self.add_subject(selected_subject)
            available_subjects.remove(selected_subject)

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
            theme_record = self.get_by_id(Theme,theme_id, id_field="theme_id")
            if theme_record:
                if theme_name: theme_record.theme_name = theme_name
                session.commit()

    def delete_theme(self, theme_id):
        with self.Session() as session:
            theme_record = self.get_by_id(Theme,theme_id, id_field="theme_id")
            if theme_record:
                session.delete(theme_record)
                session.commit()

    def add_initial_themes(self):
        for i in range(len(themes_data)):
            self.add_theme(themes_data[i])

    def display_all_themes(self):
        themes = self.get_all(Theme)
        for theme in themes:
            print(f"ID Темы: {theme.theme_id}, Название: {theme.theme_name}")

    def add_theme_for_app(self, theme_id,theme_name):
        with self.Session() as session:
            new_theme = Theme(theme_id=theme_id, theme_name=theme_name)
            session.add(new_theme)
            session.commit()


class AdviserThemeRepository(BaseRepository):
    def __init__(self, engine, adviser_repository, theme_repository):
        super().__init__(engine)
        self.adviser_repository = adviser_repository
        self.theme_repository = theme_repository

    def delete_adviser_theme(self, adviser_id, theme_id):
        with self.Session() as session:
            delete_adviser_theme_priority = session.query(AdviserTheme).filter(
                AdviserTheme.adviser_id == adviser_id,
                AdviserTheme.theme_id == theme_id,
            ).first()
            if delete_adviser_theme_priority:
                session.delete(delete_adviser_theme_priority)
                session.commit()

    def display_all_adviser_themes(self):
        adviser_themes = self.get_all(AdviserTheme)
        for adviser_theme in adviser_themes:
            print(
                f"ID: {adviser_theme.adviser_theme_id}, ID Научного руководителя: {adviser_theme.adviser_id}, "
                f"ID Темы: {adviser_theme.theme_id}"
            )

    def add_adviser_themes(self, adviser_id, *theme_ids):
        with self.Session() as session:
            for theme_id in theme_ids:
                new_adviser_theme = AdviserTheme(adviser_id=adviser_id, theme_id=theme_id)
                session.add(new_adviser_theme)
            session.commit()

    def update_adviser_themes(self, adviser_id, *new_theme_ids):
        print(f"Обновление тем для научного руководителя ID {adviser_id}: {new_theme_ids}")
        with self.Session() as session:
            # Удаляем старые темы
            session.query(AdviserTheme).filter(AdviserTheme.adviser_id == adviser_id).delete()

            # Добавляем новые темы
            for theme_id in new_theme_ids:
                new_adviser_theme = AdviserTheme(adviser_id=adviser_id, theme_id=theme_id)
                session.add(new_adviser_theme)

            session.commit()


class ThemeSubjectImportanceRepository(BaseRepository):
    def __init__(self, engine, theme_repository, subject_repository):
        super().__init__(engine)
        self.theme_repository = theme_repository
        self.subject_repository = subject_repository

    def add_theme_subject_importance(self, theme_id, subject_id, weight):
        with self.Session() as session:
            try:
                # Проверяем, существует ли запись для данной темы и предмета
                existing_record = session.query(ThemeSubjectImportance).filter_by(
                    theme_id=theme_id,
                    subject_id=subject_id
                ).first()

                if existing_record:
                    # Если запись существует, обновляем её вес
                    existing_record.weight = weight
                    print(f"Обновлено: Тема ID: {theme_id}, Предмет ID: {subject_id}, Новый вес: {weight}")
                else:
                    # Если записи нет, создаем новую
                    new_record = ThemeSubjectImportance(
                        theme_id=theme_id,
                        subject_id=subject_id,
                        weight=weight
                    )
                    session.add(new_record)
                    #print(f"Добавлено: Тема ID: {theme_id}, Предмет ID: {subject_id}, Вес: {weight}")

                session.commit()  # Сохраняем изменения
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при добавлении/обновлении важности: {e}")

    def update_theme_subject_importance(self, theme_subject_importance_id, theme_id=None, subject_id=None, weight=None):
        with self.Session() as session:
            theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance,theme_subject_importance_id, id_field="theme_subject_importance_id")
            if theme_subject_importance_record:
                if theme_id is not None: theme_subject_importance_record.theme_id = theme_id
                if subject_id is not None: theme_subject_importance_record.subject_id = subject_id
                if weight is not None: theme_subject_importance_record.weight = weight
                session.commit()

    def delete_theme_subject_importance(self, theme_subject_importance_id):
        with self.Session() as session:
            theme_subject_importance_record = self.get_by_id(ThemeSubjectImportance,theme_subject_importance_id, id_field="theme_subject_importance_id")
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
        for theme in themes:
            with self.Session() as delete_session:
                try:
                    # Удаляем существующие записи для данной темы
                    delete_session.query(ThemeSubjectImportance).filter(
                        ThemeSubjectImportance.theme_id == theme.theme_id).delete()
                    delete_session.commit()  # Коммитим изменения
                except Exception as e:
                    delete_session.rollback()
                    print(f"Ошибка при удалении: {e}")
                    continue  # Переходим к следующей теме

            with self.Session() as add_session:
                try:
                    subject_count = rnd.randint(min_count, max_count)
                    subject_count = min(subject_count, len(subjects))
                    selected_subjects = rnd.sample(subjects, subject_count)

                    weights = [rnd.uniform(0.1, 1.0) for _ in selected_subjects]
                    total_weight = sum(weights)

                    # Нормализуем веса
                    normalized_weights = [weight / total_weight for weight in weights]

                    # Проверка на сумму весов
                    assert abs(sum(normalized_weights) - 1.0) < 1e-6, "Сумма нормализованных весов не равна 1"

                    for subject, normalized_weight in zip(selected_subjects, normalized_weights):
                        self.add_theme_subject_importance(theme.theme_id, subject.subject_id, normalized_weight)

                    add_session.commit()
                except Exception as e:
                    add_session.rollback()
                    print(f"Ошибка при добавлении: {e}")


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
            student_subject_grade_record = self.get_by_id(StudentSubjectGrade,student_subject_grade_id, id_field="student_subject_grade_id")
            if student_subject_grade_record:
                if student_id is not None: student_subject_grade_record.student_id = student_id
                if subject_id is not None: student_subject_grade_record.subject_id = subject_id
                if grade is not None: student_subject_grade_record.grade = grade
                session.commit()

    def delete_student_subject_grade(self, student_subject_grade_id):
        with self.Session() as session:
            student_subject_grade_record = self.get_by_id(StudentSubjectGrade,student_subject_grade_id, id_field="student_subject_grade_id")
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

    def update_student_theme_interest(self, student_id, theme_id, interest_level):
        with self.Session() as session:
            student_theme_interest = StudentThemeInterest(student_id=student_id, theme_id=theme_id, interest_level=interest_level)
            session.add(student_theme_interest)
            session.commit()

    def generate_random_interests(self):
        with self.Session() as session:
            available_themes = session.query(Theme).all()
            selected_themes = rnd.sample(available_themes, 5)
            interest_levels = [1, 2, 3, 4, 5]
            rnd.shuffle(interest_levels)
            interests = [(theme.theme_id, level) for theme, level in zip(selected_themes, interest_levels)]
            return interests

    def initialize_student_interests(self):
        students = self.student_repository.get_all(Student)
        for student in students:
            interests = self.generate_random_interests()
            self.add_multiple_student_theme_interests(student.student_id, interests)

    def add_multiple_student_theme_interests(self, student_id, interests):
        with self.Session() as session:
            try:
                for theme_id, interest_level in interests:
                    self.add_student_theme_interest(student_id, theme_id, interest_level)
            except Exception as e:
                session.rollback()
                print(f"Ошибка при добавлении интересов: {e}")

    def display_all_student_theme_interests(self):
        student_theme_interests = self.get_all(StudentThemeInterest)
        for interest in student_theme_interests:
            print(
                f"ID: {interest.student_theme_interest_id}, ID Студента: {interest.student_id}, "
                f"ID Темы: {interest.theme_id}, Уровень интереса: {interest.interest_level}")

    def get_selected_themes_for_student(self, student_id):
        with self.Session() as session:
            return session.query(Theme).join(StudentThemeInterest).filter(
                StudentThemeInterest.student_id == student_id).all()


class DistributionAlgorithmRepository(BaseRepository):
    def __init__(self, engine, student_subject_grade_repository, student_theme_interest_repository,
                 theme_subject_importance_repository, adviser_theme_repository, distribution_repository):
        super().__init__(engine)
        self.distribution_repository = distribution_repository
        self.student_grade_record_repository = student_subject_grade_repository
        self.student_theme_interest_repository = student_theme_interest_repository
        self.theme_subject_importance_repository = theme_subject_importance_repository
        self.adviser_theme_repository = adviser_theme_repository
        self.advisers = {}

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

            # Логирование суммарных взвешенных оценок
            # print("\nСуммарные взвешенные оценки:")
            # for key, score in suitability_scores.items():
            #     print(f"Тема ID: {key[0]}, Студент ID: {key[1]}, Взвешенная оценка: {round(score, 2)}")

            for key in suitability_scores:
                max_possible_score = sum(weight * 5 for weight in subject_weights[key[0]].values())
                normalized_score = (suitability_scores[key] / max_possible_score) * 100 if max_possible_score > 0 else 0
                suitability_scores[key] = round(normalized_score, 2)

            # # Логирование нормализованных оценок
            # print("\nНормализованные оценки соответствия:")
            # for key, score in suitability_scores.items():
            #     print(f"Тема ID: {key[0]}, Студент ID: {key[1]}, Степень подходимости студента к теме: {score:.2f}%")

        return suitability_scores

    def link_weighted_grades_with_interest(self):
        student_scores = {}  # Словарь для хранения данных о студентах
        with self.student_theme_interest_repository.Session() as session:
            suitability_scores = self.link_theme_subject_importance_with_student_subject_grade()
            student_theme_interests = session.query(StudentThemeInterest).all()

            # Сбор всех интересов студентов
            for (theme_id, student_id), suitability_score in suitability_scores.items():
                interest_level = next((interest.interest_level for interest in student_theme_interests
                                       if interest.student_id == student_id and interest.theme_id == theme_id), None)
                if interest_level is not None:
                    # Сохраняем в словаре кортеж (степень подходимости, уровень интереса)
                    student_scores[student_id] = student_scores.get(student_id, [])
                    student_scores[student_id].append((theme_id, suitability_score, interest_level))

            sorted_results = []
            for student_id, scores in student_scores.items():
                sorted_scores = sorted(scores, key=lambda x: ( x[2]))
                sorted_results.extend([(student_id, theme_id, suitability_score, interest_level) for
                                       theme_id, suitability_score, interest_level in sorted_scores])

            print("\nРезультаты соответствия тем и интересов студентов:")
            for student_id, theme_id, suitability_score, interest_level in sorted_results:
                print(f"Студент ID: {student_id}, Тема ID: {theme_id}, "
                      f"Степень подходимости: {round(suitability_score, 2)}%, "
                      f"Уровень интереса: {interest_level}")

        return sorted_results  # Возвращаем отсортированные результаты

    def prepare_advisers_and_themes(self):
        """
        Подготавливает данные о научных руководителях и их темах.
        """
        with self.Session() as session:
            advisers = {adv.adviser_id: adv for adv in session.query(Adviser).all()}
            adviser_themes = defaultdict(list)
            for adv_theme in session.query(AdviserTheme).all():
                adviser_themes[adv_theme.adviser_id].append(adv_theme.theme_id)
            return advisers, adviser_themes

    def create_priority_queues(self, sorted_results):
        """
        Создает очереди приоритетов для тем на основе результатов соответствия.
        """
        theme_priority_queues = defaultdict(list)
        student_entries = defaultdict(list)

        for student_id, theme_id, suitability, interest in sorted_results:
            heapq.heappush(theme_priority_queues[theme_id], (-suitability, student_id))
            student_entries[student_id].append((suitability, theme_id, interest))

        return theme_priority_queues, student_entries

    def assign_students(self, student_entries, advisers, adviser_themes, theme_priority_queues, adviser_assignments,
                        session=None):
        """
        Основной цикл для распределения студентов по научным руководителям и темам.
        """
        if session is None:
            raise ValueError("Session должна быть передана для обновления данных в базе.")

        assigned_students = set()
        distributions = []
        reprocess_queue = deque()

        for student_id in student_entries:
            if student_id in assigned_students:
                continue
            for interest_level in range(1, 6):
                themes = [
                    (suit, theme, int_level)
                    for suit, theme, int_level in student_entries[student_id]
                    if int_level == interest_level
                ]
                if not themes:
                    continue
                best_theme = max(themes, key=lambda x: x[0])[1]
                if self.assign_with_replacement(
                        student_id,
                        best_theme,
                        themes[0][0],
                        advisers,
                        adviser_themes,
                        theme_priority_queues,
                        adviser_assignments,
                        assigned_students,
                        distributions,
                        reprocess_queue,
                        session=session  # Передаем session
                ):
                    break
        return assigned_students, distributions, reprocess_queue

    def process_reprocess_queue(self, reprocess_queue, student_entries, advisers, adviser_themes,
                                theme_priority_queues, assigned_students, distributions, adviser_assignments,
                                session=None):
        if session is None:
            raise ValueError("Session должна быть передана для обновления данных в базе.")

        while reprocess_queue:
            student_id = reprocess_queue.popleft()
            if student_id in assigned_students:
                continue

            for interest_level in range(1, 6):
                themes = [
                    (suit, theme, int_level)
                    for suit, theme, int_level in student_entries[student_id]
                    if int_level == interest_level
                ]
                if not themes:
                    continue

                best_theme = max(themes, key=lambda x: x[0])[1]
                if self.assign_with_replacement(
                        student_id,
                        best_theme,
                        themes[0][0],
                        advisers,
                        adviser_themes,
                        theme_priority_queues,
                        adviser_assignments,
                        assigned_students,
                        distributions,
                        session=session
                ):
                    break

    def assign_with_replacement(self, student_id, theme_id, suitability, advisers, adviser_themes,
                                theme_priority_queues, adviser_assignments, assigned_students, distributions,
                                reprocess_queue=None, session=None):
        if reprocess_queue is None:
            reprocess_queue = deque()
        if session is None:
            raise ValueError("Session должна быть передана для обновления данных в базе.")

        available_advisers = [
            adv_id for adv_id in adviser_themes
            if theme_id in adviser_themes[adv_id] and advisers[adv_id].number_of_places > 0
        ]

        if available_advisers:
            adv_id = available_advisers[0]
            adviser_assignments[adv_id].append(student_id)
            heapq.heappush(theme_priority_queues[theme_id], (-suitability, student_id))
            distributions.append({
                "theme_id": theme_id,
                "student_id": student_id,
                "adviser_id": adv_id
            })
            assigned_students.add(student_id)

            # Уменьшаем число мест у научного руководителя
            adviser = advisers[adv_id]
            adviser.number_of_places -= 1
            session.commit()

            return True
        else:
            if theme_priority_queues[theme_id]:
                lowest_suit, existing_student = heapq.heappop(theme_priority_queues[theme_id])
                lowest_suit = -lowest_suit
                if suitability > lowest_suit:
                    replaced_adv_id = None
                    for adv_id in adviser_assignments:
                        if existing_student in adviser_assignments[adv_id]:
                            adviser_assignments[adv_id].remove(existing_student)
                            replaced_adv_id = adv_id
                            break

                    if replaced_adv_id is not None:
                        # Восстанавливаем место для старого научного руководителя
                        replaced_adviser = advisers[replaced_adv_id]
                        replaced_adviser.number_of_places += 1
                        session.commit()

                    # Назначаем нового студента
                    adv_id = next(
                        adv_id for adv_id in adviser_assignments
                        if existing_student in adviser_assignments[adv_id]
                    )
                    adviser_assignments[adv_id].append(student_id)
                    heapq.heappush(theme_priority_queues[theme_id], (-suitability, student_id))
                    distributions.append({
                        "theme_id": theme_id,
                        "student_id": student_id,
                        "adviser_id": adv_id
                    })
                    assigned_students.add(student_id)

                    # Уменьшаем число мест у нового научного руководителя
                    adviser = advisers[adv_id]
                    adviser.number_of_places -= 1
                    session.commit()

                    if existing_student not in assigned_students:
                        reprocess_queue.append(existing_student)
                    return True
                else:
                    heapq.heappush(theme_priority_queues[theme_id], (-lowest_suit, existing_student))
        return False

    def handle_unassigned_students(self, unassigned_students, student_entries, advisers, adviser_themes,
                                   adviser_assignments, distributions, session):
        """
        Обрабатывает студентов, которые остались нераспределенными.
        Возвращает список студентов, которые так и не были назначены.
        """
        remain_students = set()  # Список для хранения оставшихся студентов

        for student_id in unassigned_students:
            logging.debug(f"Обработка нераспределенного Студента ID: {student_id}")

            available_themes = [theme_id for suit, theme_id, int_level in student_entries[student_id]]
            logging.debug(f"Доступные темы для Студента ID: {student_id}: {available_themes}")

            available_advisers = [
                adv_id for adv_id in adviser_themes
                if set(adviser_themes[adv_id]) & set(available_themes) and len(adviser_assignments[adv_id]) < advisers[
                    adv_id].number_of_places
            ]
            logging.debug(
                f"Доступные научные руководители для Студента ID: {student_id}: {available_advisers}")

            if not available_advisers:
                logging.debug(f"Нет доступных научных руководителей для Студента ID: {student_id}")
                remain_students.add(student_id)
                continue

            best_adv = max(
                available_advisers,
                key=lambda x: (advisers[x].number_of_places - len(adviser_assignments[x]), x)
            )
            common_theme = next(theme for theme in adviser_themes[best_adv] if theme in available_themes)
            logging.debug(
                f"Студент ID: {student_id} назначен на Тему ID: {common_theme}, Научный руководитель ID: {best_adv}")

            # Назначаем студента
            adviser_assignments[best_adv].append(student_id)
            distributions.append({
                "student_id": student_id,
                "theme_id": common_theme,
                "adviser_id": best_adv
            })

        return remain_students  # Возвращаем список оставшихся студентов

    def assign_students_to_advisers_and_distribute(self):
        sorted_results = self.link_weighted_grades_with_interest()
        with self.Session() as session:
            advisers, adviser_themes = self.prepare_advisers_and_themes()
            theme_priority_queues, student_entries = self.create_priority_queues(sorted_results)
            adviser_assignments = defaultdict(list)

            # Распределение студентов
            assigned_students, distributions, reprocess_queue = self.assign_students(
                student_entries, advisers, adviser_themes, theme_priority_queues, adviser_assignments, session
            )

            # Обработка очереди повторной обработки
            self.process_reprocess_queue(
                reprocess_queue, student_entries, advisers, adviser_themes, theme_priority_queues, assigned_students,
                distributions, adviser_assignments, session
            )

            all_students = {s.student_id for s in self.get_all(Student)}
            unassigned_students = all_students - assigned_students

            # Обработка нераспределенных студентов
            remain_students = self.handle_unassigned_students(unassigned_students, student_entries, advisers, adviser_themes,
                                            adviser_assignments, distributions, session)



            # self.handle_overbooked_students(remain_students, student_entries, advisers, adviser_themes,
            #                                 adviser_assignments, distributions, session)

            # Сохраняем распределения
            self.distribution_repository.add_distribution(distributions)

            # Синхронизируем количество мест у научных руководителей в базе данных
            self.finalize_adviser_places(advisers, session=session)

            # Логирование финального состояния
            logging.debug("Финальное состояние научных руководителей:")
            for adv_id, adviser in advisers.items():
                logging.debug(f"ID Руководителя: {adv_id}, Мест: {adviser.number_of_places}")

            return unassigned_students

    def finalize_adviser_places(self, advisers, session=None):
        """
        Синхронизирует количество мест у научных руководителей в базе данных.
        """
        if session is None:
            raise ValueError("Session должна быть передана для обновления данных в базе.")

        try:
            for adv_id, adviser in advisers.items():
                # Обновляем поле number_of_places в базе данных
                db_adviser = session.query(Adviser).get(adv_id)
                if db_adviser:
                    db_adviser.number_of_places = adviser.number_of_places
                    logging.debug(
                        f"Обновлено количество мест для Научного руководителя ID: {adv_id}, Мест: {adviser.number_of_places}")
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка при обновлении количества мест у научных руководителей: {e}")

    def handle_overbooked_students(self, unassigned_students, student_entries, advisers, adviser_themes,
                                   adviser_assignments, distributions, session=None):
        """
        Обрабатывает студентов, у которых все темы заняты, назначая их к наиболее свободному научному руководителю.
        """
        if session is None:
            raise ValueError("Session должна быть передана для обновления данных в базе.")

        for student_id in unassigned_students:
            available_themes = [theme_id for suit, theme_id, int_level in student_entries[student_id]]
            available_advisers = [
                adv_id for adv_id in adviser_themes
                if set(adviser_themes[adv_id]) & set(available_themes) and advisers[adv_id].number_of_places > 0
            ]

            if not available_advisers:
                # Все темы заняты, ищем наиболее свободного научного руководителя
                most_available_adviser = max(
                    advisers.values(),
                    key=lambda adv: (adv.number_of_places, adv.adviser_id)
                )

                if most_available_adviser.number_of_places > 0:
                    # Выбираем любую тему, связанную с этим научным руководителем
                    common_theme = next(theme for theme in adviser_themes[most_available_adviser.adviser_id])
                    adviser_assignments[most_available_adviser.adviser_id].append(student_id)
                    distributions.append({
                        "theme_id": common_theme,
                        "student_id": student_id,
                        "adviser_id": most_available_adviser.adviser_id
                    })

                    # Уменьшаем число мест у научного руководителя
                    most_available_adviser.number_of_places -= 1
                    session.commit()

                    logging.info(
                        f"Студент ID: {student_id} назначен Научному руководителю ID: {most_available_adviser.adviser_id}, "
                        f"Тема ID: {common_theme}")
                else:
                    logging.warning(
                        f"Невозможно назначить Студента ID: {student_id}, нет свободных мест ни у одного научного руководителя.")
            else:
                # Есть доступные места для тем студента
                best_adv = max(
                    available_advisers,
                    key=lambda x: (advisers[x].number_of_places, x)
                )
                common_theme = next(theme for theme in adviser_themes[best_adv] if theme in available_themes)
                adviser_assignments[best_adv].append(student_id)
                distributions.append({
                    "theme_id": common_theme,
                    "student_id": student_id,
                    "adviser_id": best_adv
                })

                # Уменьшаем число мест у научного руководителя
                adviser = advisers[best_adv]
                adviser.number_of_places -= 1
                session.commit()

                logging.info(
                    f"Студент ID: {student_id} назначен Научному руководителю ID: {best_adv}, Тема ID: {common_theme}")

class DistributionRepository(BaseRepository):
    def __init__(self, engine):
        super().__init__(engine)
        self.Session = sessionmaker(bind=engine)

    def add_distribution(self, distributions):
        with self.Session() as session:
            try:
                for distribution in distributions:
                    new_distribution = Distribution(
                        student_id=distribution["student_id"],
                        theme_id=distribution["theme_id"],
                        adviser_id=distribution["adviser_id"],
                        #interest_level = distribution["interest_level"]
                    )
                    session.add(new_distribution)
                session.commit()
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при добавлении распределений: {e}")

    def add_distribution_for_app(self,student_id, theme_id, adviser_id):
        with self.Session() as session:
            new_distribution = Distribution(student_id=student_id,theme_id=theme_id,adviser_id=adviser_id)
            session.add(new_distribution)
            session.commit()

    def display_all_distributions(self):
        with self.Session() as session:
            try:
                all_distributions = session.query(Distribution).order_by(Distribution.student_id).all()

                if not all_distributions:
                    return []

                distributions_data = [
                    {
                        "distribution_id": distribution.distribution_id,
                        "student_id": distribution.student_id,
                        "theme_id": distribution.theme_id,
                        "adviser_id": distribution.adviser_id,
                    }
                    for distribution in all_distributions
                ]
                return distributions_data

            except Exception as e:
                logging.error(f"Ошибка при получении распределений: {e}")
                return []

    def update_distribution(self, distribution_id, student_id, theme_id, adviser_id):
        session = self.Session()
        try:
            distribution = session.query(Distribution).filter(Distribution.distribution_id == distribution_id).first()
            if distribution:
                distribution.student_id = student_id
                distribution.theme_id = theme_id
                distribution.adviser_id = adviser_id
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при обновлении распределений: {e}")
        finally:
            session.close()

    def delete_distribution(self, distribution_id):
        session = self.Session()
        try:
            distribution = self.get_by_id(Distribution, distribution_id, id_field='distribution_id')
            if distribution:
                session.delete(distribution)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении распределения: {e}")
            return False
        finally:
            session.close()

