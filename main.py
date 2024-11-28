from sqlalchemy import create_engine
from models import Base
from repositories import *
import random as rnd

def main():
    engine = create_engine('sqlite:///database.db')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Создаем экземпляры репозиториев
    student_repository = StudentRepository(engine)
    subject_repository = SubjectRepository(engine)
    adviser_repository = AdviserRepository(engine)
    theme_repository = ThemeRepository(engine)
    theme_subject_importance_repository = ThemeSubjectImportanceRepository(engine, theme_repository, subject_repository)
    student_subject_grade_repository = StudentSubjectGradeRepository(engine, student_repository, subject_repository)
    student_theme_interest_repository = StudentThemeInterestRepository(engine, student_repository, theme_repository)
    adviser_theme_repository = AdviserThemeRepository(engine, adviser_repository, theme_repository)
    distribution_repository = DistributionRepository(engine)
    distribution_algorithm_repository = DistributionAlgorithmRepository(engine, student_subject_grade_repository, student_theme_interest_repository,
                                      theme_subject_importance_repository, adviser_theme_repository, distribution_repository)

    # Очищаем репозитории
    student_repository.delete_all(Student)
    subject_repository.delete_all(Subject)
    adviser_repository.delete_all(Adviser)
    theme_repository.delete_all(Theme)
    theme_subject_importance_repository.delete_all(ThemeSubjectImportance)
    student_subject_grade_repository.delete_all(StudentSubjectGrade)
    student_theme_interest_repository.delete_all(StudentThemeInterest)
    adviser_theme_repository.delete_all(AdviserTheme)
    distribution_repository.delete_all(Distribution)

    # Добавляем начальные данные
    student_repository.add_initial_students(30)
    subject_repository.add_initial_subjects()
    adviser_repository.add_initial_advisers()
    theme_repository.add_initial_themes()

    # Получаем данные из репозиториев
    students = student_repository.get_all(Student)
    subjects = subject_repository.get_all(Subject)
    themes = theme_repository.get_all(Theme)

    for student in students:
        for subject in subjects:
            grade = rnd.randint(3, 5)
            student_subject_grade_repository.add_student_subject_grade(student.student_id, subject.subject_id, grade)

    for theme in themes:
        for subject in subjects:
            weight = rnd.uniform(0.1, 1)
            theme_subject_importance_repository.add_theme_subject_importance(theme.theme_id, subject.subject_id, weight)

    #добавление тем научным руководителям
    adviser_theme_repository.add_adviser_themes(1, *[1])
    adviser_theme_repository.add_adviser_themes(2, *[2])
    adviser_theme_repository.add_adviser_themes(3, *[3, 4])
    adviser_theme_repository.add_adviser_themes(4, *[5, 6])
    adviser_theme_repository.add_adviser_themes(5, *[7, 8])
    adviser_theme_repository.add_adviser_themes(6, *[9, 10, 11])
    adviser_theme_repository.add_adviser_themes(7, *[12, 13])
    adviser_theme_repository.add_adviser_themes(8, *[14, 15, 16, 17])
    adviser_theme_repository.add_adviser_themes(9, *[18, 19])
    adviser_theme_repository.add_adviser_themes(10, *[20,21,22])
    adviser_theme_repository.add_adviser_themes(11, *[23])
    adviser_theme_repository.add_adviser_themes(12, *[7, 8])
    adviser_theme_repository.add_adviser_themes(13, *[19, 24, 25])
    adviser_theme_repository.add_adviser_themes(14, *[26, 27])
    adviser_theme_repository.add_adviser_themes(15, *[28])


    theme_subject_importance_repository.add_random_importances_for_themes(themes, subjects)
    student_theme_interest_repository.initialize_student_interests()

    # Выводим информацию
    print("Студенты:")
    student_repository.display_all_students()
    print("\nПредметы:")
    subject_repository.display_all_subjects()
    print("\nНаучные руководители:")
    adviser_repository.display_all_advisers()
    print("\nТемы:")
    theme_repository.display_all_themes()
    print("\nИнтересы студентов к темам:")
    student_theme_interest_repository.display_all_student_theme_interests()
    print("\nСвязь тем и научных руководителей:")
    adviser_theme_repository.display_all_adviser_themes()
    print("\nВеса предметов по темам:")
    theme_subject_importance_repository.display_all_theme_subject_importances()

    unassigned_students = distribution_algorithm_repository.assign_students_to_advisers_and_distribute()

    print("\nИтоговые распределения")
    distribution_repository.display_all_distributions()


    if unassigned_students:
        print("\nНеназначенные студенты:")
        check_unassigned_students(unassigned_students, adviser_repository, student_theme_interest_repository,
                                  student_repository)


def check_unassigned_students(unassigned_students, adviser_repository, student_theme_interest_repository, student_repository):
    for student_id in unassigned_students:
        student = student_repository.get_by_student_id(student_id)
        if student:
            print(f"\nСтудент ID: {student.student_id}, Имя: {student.firstname} {student.lastname}")

            # Получаем темы, к которым у студента есть интересы
            selected_themes = student_theme_interest_repository.get_selected_themes_for_student(student.student_id)
            if selected_themes:
                print("  Темы интересов:")
                for theme in selected_themes:
                    print(f"    - Тема ID: {theme.theme_id}, Название: {theme.theme_name}")
            else:
                print("  У студента нет тем интересов.")

            # Проверяем наличие научных советников для выбранных тем
            for theme in selected_themes:
                advisers = adviser_repository.get_advisers_for_theme(theme.theme_id)
                if not advisers:
                    print(f"  Нет научных советников для темы ID: {theme.theme_id}")
                else:
                    for adviser in advisers:
                        print(f"  Научный советник ID: {adviser.adviser_id} доступен для темы ID: {theme.theme_id} "
                              f"(оставшиеся места: {adviser.number_of_places})")
                        if adviser.number_of_places <= 0:
                            print(f"  У научного советника ID: {adviser.adviser_id} нет свободных мест для темы ID: {theme.theme_id}")
if __name__ == "__main__":
    main()