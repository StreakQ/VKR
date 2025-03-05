from repositories import *


def link_theme_subject_importance_with_student_subject_grade(self):
    suitability_scores = {}

    # Получение записей из репозиториев
    with self.student_grade_record_repository.Session() as session:
        theme_subject_importance_records = session.query(ThemeSubjectImportance).all()
        student_subject_grade_records = session.query(StudentSubjectGrade).all()

        # Создание словаря весов предметов
        subject_weights = {}
        for importance in theme_subject_importance_records:
            subject_weights.setdefault(importance.theme_id, {})[importance.subject_id] = importance.weight

        # Создание словаря оценок студентов по предметам
        student_grades = {}
        for grade_record in student_subject_grade_records:
            student_grades.setdefault(grade_record.student_id, {})[grade_record.subject_id] = grade_record.grade

        # Вычисление взвешенных оценок
        for theme_id, subjects in subject_weights.items():
            for subject_id, weight in subjects.items():
                for student_id, grades in student_grades.items():
                    if subject_id in grades:
                        weighted_grade = grades[subject_id] * weight
                        suitability_scores.setdefault((theme_id, student_id), 0)
                        suitability_scores[(theme_id, student_id)] += weighted_grade

        # Нормализация оценок
        for key in suitability_scores:
            max_possible_score = sum(weight * 5 for weight in subject_weights[key[0]].values())
            normalized_score = (suitability_scores[key] / max_possible_score) * 100 if max_possible_score > 0 else 0
            suitability_scores[key] = round(normalized_score, 2)

    return suitability_scores


def link_weighted_grades_with_interest(self):
    result = []

    with self.student_theme_interest_repository.Session() as session:
        suitability_scores = self.link_theme_subject_importance_with_student_subject_grade()
        student_theme_interests = session.query(StudentThemeInterest).all()

        # Создание словаря интересов студентов
        interest_dict = {(interest.student_id, interest.theme_id): interest.interest_level for interest in
                         student_theme_interests}

        for (theme_id, student_id), suitability_score in suitability_scores.items():
            interest_level = interest_dict.get((student_id, theme_id))
            if interest_level is not None:
                result.append((theme_id, student_id, suitability_score, interest_level))

        # Сортировка результатов
        result.sort(key=lambda x: (-x[2], x[3], x[0], x[1]))

        print("\nРезультаты соответствия тем и интересов студентов:")
        for theme_id, student_id, suitability_score, interest_level in result:
            print(f"Студент ID: {student_id}, Тема ID: {theme_id}, "
                  f"Степень подходимости: {round(suitability_score, 2)}%, "
                  f"Уровень интереса: {interest_level}")

    return result

def assign_student_evenly(student_id, theme_id, interest_level, advisers, adviser_themes,
                          adviser_assignments, distributions_to_add, session, adviser_repository):
    # Словарь для отслеживания количества назначений
    adviser_load = {adviser.adviser_id: 0 for adviser in advisers.values()}

    # Обновляем количество назначений для каждого научного руководителя
    for distribution in distributions_to_add:
        adviser_load[distribution["adviser_id"]] += 1

    # Находим научного руководителя с наименьшей нагрузкой
    available_advisers = [
        adviser for adviser in advisers.values()
        if adviser.number_of_places > 0 and
           adviser_load[adviser.adviser_id] < adviser.number_of_places and
           theme_id in adviser_themes[adviser.adviser_id]
    ]

    if available_advisers:
        adviser = min(available_advisers, key=lambda x: adviser_load[x.adviser_id])

        distribution_entry = {
            "theme_id": theme_id,
            "student_id": student_id,
            "adviser_id": adviser.adviser_id,
            "interest_level": interest_level
        }

        distributions_to_add.append(distribution_entry)

        # Уменьшаем количество мест у научного руководителя
        adviser_repository.decrease_adviser_places(adviser.adviser_id, session)

        return True

    return False

def assign_students_to_advisers_and_distribute(self):
    suitability_results = self.link_weighted_grades_with_interest()
    sorted_results = sorted(suitability_results, key=lambda x: (x[3], -x[2], x[0]))

    unassigned_students = set()
    assigned_students = set()
    distributions_to_add = []

    with self.student_theme_interest_repository.Session() as session:
        advisers = {adviser.adviser_id: adviser for adviser in session.query(Adviser).all()}
        adviser_themes = {
            adviser.adviser_id: [
                adviser_theme.theme_id for adviser_theme in session.query(AdviserTheme).filter(
                    AdviserTheme.adviser_id == adviser.adviser_id).all()
            ] for adviser in advisers.values()
        }

        adviser_repository = AdviserRepository(session)

        # Создаем словарь интересов студентов для быстрого доступа
        student_interests = {
            (interest.student_id, interest.theme_id): interest.interest_level
            for interest in session.query(StudentThemeInterest).all()
        }

        for theme_id, student_id, total_weighted_grade, interest_level in sorted_results:
            if student_id in assigned_students:
                continue

            if (student_id, theme_id) not in student_interests:
                continue

            if self.assign_student_to_adviser(student_id, theme_id, interest_level, advisers,
                                              adviser_themes, distributions_to_add, session, adviser_repository):
                assigned_students.add(student_id)
            else:
                # Попытка назначить студента на альтернативные темы
                self.try_assign_alternative_themes(student_id, interest_level, assigned_students, advisers,
                                                    adviser_themes, distributions_to_add, session, adviser_repository)

        self.distribution_repository.add_distribution(distributions_to_add)

        # Добавление не назначенных студентов
        all_students = session.query(Student).all()
        unassigned_students.update(student.student_id for student in all_students if student.student_id not in assigned_students)

    return unassigned_students

def try_assign_alternative_themes(self, student_id, interest_level, assigned_students, advisers,
                                   adviser_themes, distributions_to_add, session, adviser_repository):
    for new_interest_level in range(interest_level + 1, 6):
        alternative_themes = [
            interest.theme_id for interest in session.query(StudentThemeInterest).filter(
                StudentThemeInterest.student_id == student_id,
                StudentThemeInterest.interest_level == new_interest_level
            ).all()
        ]

        for new_theme_id in alternative_themes:
            if student_id in assigned_students:
                return

            if self.assign_student_to_adviser(student_id, new_theme_id, new_interest_level, advisers,
                                              adviser_themes, distributions_to_add, session, adviser_repository):
                assigned_students.add(student_id)
                return


