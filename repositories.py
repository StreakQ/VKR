from importlib.metadata import distribution

from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker
from models import (Student, Adviser, Subject, Theme,
                    ThemeSubjectImportance, StudentSubjectGrade, StudentThemeInterest, Distribution, AdviserTheme, DistributionAlgorithm)
from faker import Faker
import random as rnd
import logging
from data import *
from collections import defaultdict, deque
import heapq

fake = Faker('ru_RU')

class BaseRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def get_all(self, model):
        with self.Session() as session:
            return session.query(model).all()

    def get_by_id(self, model, record_id, id_field='student_id'):
        with self.Session() as session:
            return session.query(model).filter(getattr(model, id_field) == record_id).first()


    def delete_all(self, model):
        with self.Session() as session:
            try:
                session.query(model).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def get_all_without_close(self, model):
        return self.session.query(model).all()


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
            student = self.get_by_id(Student,student_id, id_field="student_id")
            if student:
                if firstname: student.firstname = firstname
                if lastname: student.lastname = lastname
                if patronymic: student.patronymic = patronymic
                if group_student: student.group_student = group_student
                session.commit()

    def delete_student(self, student_id):
        with self.Session() as session:
            student = self.get_by_id(Student,student_id, id_field="student_id")
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
            adviser_record = self.get_by_id(Adviser,adviser_id, id_field="adviser_id")
            if adviser_record:
                if firstname: adviser_record.firstname = firstname
                if lastname: adviser_record.lastname = lastname
                if patronymic: adviser_record.patronymic = patronymic
                if number_of_places is not None: adviser_record.number_of_places = number_of_places
                session.commit()

    def delete_adviser(self, adviser_id):
        with self.Session() as session:
            adviser_record = self.get_by_id(Adviser,adviser_id, id_field="adviser_id")
            if adviser_record:
                session.delete(adviser_record)
                session.commit()

    def add_initial_advisers(self):
        for firstname, lastname, patronymic, number_of_places in advisers_data:
            self.add_adviser(firstname, lastname, patronymic, number_of_places)

    def display_all_advisers(self):
        advisers = self.get_all(Adviser)
        for adviser in advisers:
            print(
                f"ID Руководителя: {adviser.adviser_id}, Имя: {adviser.firstname} {adviser.lastname} {adviser.patronymic}, Мест: "
                f"{adviser.number_of_places}")

    def get_advisers_for_theme(self, theme_id):
        with self.Session() as session:
            return session.query(Adviser).join(AdviserTheme).filter(AdviserTheme.theme_id == theme_id).all()

    def decrease_adviser_places(self, adviser_id, session):
        adviser_record = self.get_by_adviser_id(adviser_id, session)
        if adviser_record and adviser_record.number_of_places > 0:  # Уменьшаем до 0
            print(f"Старое значение мест у ID {adviser_id}: {adviser_record.number_of_places}")
            adviser_record.number_of_places -= 1
            session.commit()
            print(f"Новое значение мест у ID {adviser_id}: {adviser_record.number_of_places}")
        else:
            print(f"Не удалось уменьшить количество мест у ID {adviser_id}. Минимум 0 мест.")

    def increase_adviser_places(self, adviser_id, session, initial_number_of_places):
        adviser_record = self.get_by_adviser_id(adviser_id, session)
        if adviser_record and adviser_record.number_of_places < initial_number_of_places:
            print(
                f"Увеличиваем места у ID {adviser_id}: {adviser_record.number_of_places} -> {adviser_record.number_of_places + 1}")
            adviser_record.number_of_places += 1
            session.commit()
        else:
            print(f"Не удалось увеличить количество мест у ID {adviser_id}. Максимум {initial_number_of_places} места.")

    def get_by_adviser_id(self, adviser_id, session):
        return session.query(Adviser).filter(Adviser.adviser_id == adviser_id).first()

    def add_adviser_for_app(self,adviser_id,firstname,lastname,patronymic,number_of_places):
        with self.Session() as session:
            new_adviser = Adviser(adviser_id=adviser_id,firstname=firstname,lastname=lastname,patronymic=patronymic,number_of_places=number_of_places)
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
        with self.Session() as session:
            # Сначала удаляем все старые темы
            session.query(AdviserTheme).filter(AdviserTheme.adviser_id == adviser_id).delete()
            self.add_adviser_themes(adviser_id, *new_theme_ids)



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

    def generate_random_interests(self):
        with self.Session() as session:
            # Получаем все доступные темы из базы данных
            available_themes = session.query(Theme).all()

            # Случайным образом выбираем 5 тем
            selected_themes = rnd.sample(available_themes, 5)

            # Генерируем уникальные уровни интереса от 1 до 5
            interest_levels = [1, 2, 3, 4, 5]
            rnd.shuffle(interest_levels)

            # Создаем список интересов
            interests = [(theme.theme_id, level) for theme, level in zip(selected_themes, interest_levels)]
            return interests

    def initialize_student_interests(self):
        students = self.student_repository.get_all(Student)
        for student in students:
            # Генерируем интересы для каждого студента
            interests = self.generate_random_interests()
            # Добавляем интересы к темам
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
    def __init__(self,engine, student_subject_grade_repository, student_theme_interest_repository,
                 theme_subject_importance_repository, adviser_theme_repository,distribution_repository):
        super().__init__(engine)
        self.distribution_repository = distribution_repository
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

    def assign_students_to_advisers_and_distribute(self, session, reprocess_queue):
        # Получаем все данные из базы
        all_students = {s.student_id for s in session.query(Student).all()}
        advisers = {a.adviser_id: a for a in session.query(Adviser).all()}
        adviser_themes = {
            adv_id: [t.theme_id for t in session.query(Theme).filter(Theme.adviser_id == adv_id).all()]
            for adv_id in advisers
        }
        student_entries = {
            s.student_id: [
                (e.suitability, e.theme_id, e.interest_level)
                for e in
                session.query(StudentThemeInterest).filter(StudentThemeInterest.student_id == s.student_id).all()
            ]
            for s in session.query(Student).all()
        }

        # Инициализация структур данных
        adviser_assignments = {adv_id: [] for adv_id in advisers}
        theme_priority_queues = defaultdict(list)
        assigned_students = set()
        distributions = []

        # Первичное распределение
        for student_id in all_students:
            themes_sorted = sorted(
                student_entries[student_id],
                key=lambda x: (x[2], -x[0]),  # Сначала по интересу, потом по пригодности
                reverse=True
            )

            for suitability, theme_id, interest_level in themes_sorted:
                if self.assign_with_replacement(
                        student_id, theme_id, suitability, advisers, adviser_themes,
                        theme_adviser_queue, adviser_assignments, theme_priority_queues,
                        assigned_students, distributions, session, reprocess_queue
                ):
                    break

        # Обработка вытесненных студентов
        while reprocess_queue:
            student_id = reprocess_queue.popleft()
            if student_id in assigned_students:
                continue

            themes_sorted = sorted(
                student_entries[student_id],
                key=lambda x: (x[2], -x[0]),  # Сначала по интересу, потом по пригодности
                reverse=True
            )

            for suitability, theme_id, interest_level in themes_sorted:
                if self.assign_with_replacement(
                        student_id, theme_id, suitability, advisers, adviser_themes,
                        theme_adviser_queue, adviser_assignments, theme_priority_queues,
                        assigned_students, distributions, session, reprocess_queue
                ):
                    break

        # Фолбэк для оставшихся студентов
        unassigned_students = all_students - assigned_students
        for student_id in unassigned_students.copy():
            themes_sorted = sorted(
                student_entries[student_id],
                key=lambda x: (x[2], -x[0]),  # Сначала по интересу, потом по пригодности
                reverse=True
            )

            for suitability, theme_id, interest_level in themes_sorted:
                if self.assign_with_replacement(
                        student_id, theme_id, suitability, advisers, adviser_themes,
                        theme_adviser_queue, adviser_assignments, theme_priority_queues,
                        assigned_students, distributions, session, reprocess_queue
                ):
                    break

        return assigned_students, distributions

    def assign_with_replacement(self, student_id, theme_id, suitability, advisers, adviser_themes,
                                theme_adviser_queue, adviser_assignments, theme_priority_queues,
                                assigned_students, distributions, session, reprocess_queue):
        # Проверяем доступных руководителей
        available_advisers = [
            adv_id for adv_id in theme_adviser_queue[theme_id]
            if len(adviser_assignments[adv_id]) < advisers[adv_id].number_of_places
        ]

        if available_advisers:
            # Выбираем первого доступного руководителя
            for adv_id in theme_adviser_queue[theme_id]:
                if len(adviser_assignments[adv_id]) < advisers[adv_id].number_of_places:
                    break
            else:
                # Если нет доступных руководителей, выходим
                return False

            # Обновляем назначения
            adviser_assignments[adv_id].append(student_id)
            heapq.heappush(theme_priority_queues[theme_id], (-suitability, student_id))
            distributions.append({
                "theme_id": theme_id,
                "student_id": student_id,
                "adviser_id": adv_id
            })
            assigned_students.add(student_id)

            # Уменьшаем количество мест у научного руководителя
            current_adviser = session.query(Adviser).get(adv_id)
            print(f"Старое значение мест у ID {adv_id}: {current_adviser.number_of_places}")
            current_adviser.number_of_places -= 1
            session.commit()
            print(f"Новое значение мест у ID {adv_id}: {current_adviser.number_of_places}")

            return True
        else:
            if theme_priority_queues[theme_id]:
                lowest_suit, existing_student = heapq.heappop(theme_priority_queues[theme_id])
                lowest_suit = -lowest_suit
                if suitability > lowest_suit:
                    print(f"Новый студент ID {student_id} имеет более высокую пригодность ({suitability})")

                    # Находим старого руководителя
                    old_adv_id = None
                    for adv_id, students in adviser_assignments.items():
                        if existing_student in students:
                            old_adv_id = adv_id
                            students.remove(existing_student)
                            break

                    if old_adv_id is None:
                        # Если старый руководитель не найден, выходим
                        return False

                    # Корректируем количество мест
                    old_adviser = session.query(Adviser).get(old_adv_id)
                    new_adviser = session.query(Adviser).get(adv_id)
                    print(f"Старое значение мест у ID {old_adv_id}: {old_adviser.number_of_places}")
                    old_adviser.number_of_places += 1
                    print(f"Новое значение мест у ID {old_adv_id}: {old_adviser.number_of_places}")

                    print(f"Старое значение мест у ID {adv_id}: {new_adviser.number_of_places}")
                    new_adviser.number_of_places -= 1
                    print(f"Новое значение мест у ID {adv_id}: {new_adviser.number_of_places}")

                    session.commit()

                    # Обновляем назначения
                    adviser_assignments[adv_id].append(student_id)
                    heapq.heappush(theme_priority_queues[theme_id], (-suitability, student_id))
                    distributions.append({
                        "theme_id": theme_id,
                        "student_id": student_id,
                        "adviser_id": adv_id
                    })
                    assigned_students.add(student_id)

                    if existing_student not in assigned_students:
                        reprocess_queue.append(existing_student)
                        print(f"Студент ID {existing_student} добавлен в очередь на повторное распределение")
                    return True
                else:
                    heapq.heappush(theme_priority_queues[theme_id], (-lowest_suit, existing_student))
            else:
                print(f"Очередь приоритетов для темы ID {theme_id} пуста")
                return False


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
                # Выполняем запрос к таблице Distribution с сортировкой
                #all_distributions = session.query(Distribution).order_by(Distribution.distribution_id).all()
                all_distributions = session.query(Distribution).order_by(Distribution.student_id).all()


                if not all_distributions:
                    print("Данных нет")
                    return  # Выход из метода, если данных нет

                for distribution in all_distributions:
                    print(f"ID: {distribution.distribution_id}, "
                          f"Студент ID: {distribution.student_id}, "
                          f"Тема ID: {distribution.theme_id}, "
                          f"Научный руководитель ID: {distribution.adviser_id}")
                          #f" Уровень интереса {distribution.interest_level}")
            except Exception as e:
                logging.error(f"Ошибка при получении распределений: {e}")

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
            print(f"Error updating distribution: {e}")
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