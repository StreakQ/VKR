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
                                      theme_subject_importance_repository, adviser_theme_repository,distribution_repository)

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
    student_repository.add_initial_students(5)
    subject_repository.add_initial_subjects(5)
    adviser_repository.add_initial_advisers(5)
    theme_repository.add_initial_themes(10)

    # Получаем данные из репозиториев
    students = student_repository.get_all(Student)
    subjects = subject_repository.get_all(Subject)
    themes = theme_repository.get_all(Theme)

    for student in students:
        for subject in subjects:
            grade = rnd.randint(3, 5)
            student_subject_grade_repository.add_student_subject_grade(student.student_id, subject.subject_id, grade)

    for student in students:
        for theme in themes:
            interest_level = rnd.randint(1, 5)
            student_theme_interest_repository.add_student_theme_interest(student.student_id, theme.theme_id, interest_level)

    for theme in themes:
        for subject in subjects:
            weight = rnd.uniform(0.1, 1)
            theme_subject_importance_repository.add_theme_subject_importance(theme.theme_id, subject.subject_id, weight)

    # Назначаем случайные темы научным руководителям
    adviser_theme_repository.assign_random_themes_to_advisers()

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
    adviser_theme_repository.display_all_adviser_theme_priorities()

    distribution_algorithm_repository.assign_students_to_advisers_and_distribute()

    print("\nИтоговые распределения")
    distribution_repository.display_all_distributions()

if __name__ == "__main__":
    main()