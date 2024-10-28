from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Импортируйте Base из вашего файла моделей
from repositories import (StudentRepository, GradeRepository, SubjectRepository,
                          AdviserRepository, ThemeRepository, AdviserGroupRepository)

def main():
    engine = create_engine("sqlite:///database.db")

    # Создаем все таблицы, если они еще не существуют
    Base.metadata.create_all(engine)  # Создаем все таблицы

    # Создаем экземпляры репозиториев
    student_repository = StudentRepository(engine)
    grade_repository = GradeRepository(engine)
    subject_repository = SubjectRepository(engine)
    adviser_repository = AdviserRepository(engine)
    theme_repository = ThemeRepository(engine)
    adviser_group_repository = AdviserGroupRepository(engine, adviser_repository)

    # Добавляем начальные данные
    student_repository.add_initial_students(10)
    grade_repository.add_initial_grades(5)
    subject_repository.add_initial_subjects(5)
    adviser_repository.add_initial_advisers(5)
    theme_repository.add_initial_themes(5)
    adviser_group_repository.add_initial_adviser_groups(5)

    # Отображаем данные
    print("Студенты:")
    student_repository.display_all_students()
    print("\nОценки:")
    grade_repository.display_all_grades()
    print("\nПредметы:")
    subject_repository.display_all_subjects()
    print("\nКонсультанты:")
    adviser_repository.display_all_advisers()
    print("\nТемы:")
    theme_repository.display_all_themes()
    print("\nГруппы консультантов:")
    adviser_group_repository.display_all_adviser_groups()

if __name__ == "__main__":
    main()