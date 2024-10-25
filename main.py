# main.py
from config import DATABASE_URL
from factories import RepositoryFactory

def main():
    # Создаем репозиторий
    student_repository = RepositoryFactory.create_student_repository(DATABASE_URL)

    # Добавляем нового студента
    student_repository.add_student("Иван", "Иванов", "Иванович", "Группа 1", 1)

    # Получаем всех студентов
    students = student_repository.get_all_students()
    for student in students:
        print(student.firstname, student.lastname)

if __name__ == "__main__":
    main()