from enum import unique
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from faker import Faker

# Импортируйте ваши модели
from models import (Base, Student, Adviser, Theme, Subject, Grade, GradeRecord,
                    StudentGradeRecord, StudentThemeInterest, ThemeSubjectImportance, AdviserGroup)

# Создание базы данных
engine = create_engine('sqlite:///vkr.db')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Инициализация Faker для генерации случайных данных
fake = Faker()

# Создание научных руководителей
advisers = []
for _ in range(10):
    adviser = Adviser(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        patronymic=fake.first_name(),
        number_of_places=random.randint(1, 5)
    )
    advisers.append(adviser)

session.add_all(advisers)
session.commit()

# Создание групп научных руководителей
adviser_groups = []
num_groups = 3
used_advisers = set()

for group_id in range(num_groups):
    unique_advisers = random.sample([adviser for adviser in advisers if adviser.adviser_id not in used_advisers],
                                    k=random.randint(1, 3))

    for adviser in unique_advisers:
        adviser_group = AdviserGroup(
            adviser_id=adviser.adviser_id,
            group_specialization=fake.word()
        )
        adviser_groups.append(adviser_group)
        used_advisers.add(adviser.adviser_id)

session.add_all(adviser_groups)
session.commit()

# Создание 20 студентов
students = []
for _ in range(20):
    student = Student(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        patronymic=fake.first_name(),
        group_student=fake.word(),
    )
    students.append(student)

session.add_all(students)
session.commit()

# Создание 30 тем
themes = []
if adviser_groups:  # Проверяем, что группы существуют
    for _ in range(30):
        theme = Theme(
            theme_name=fake.sentence(nb_words=3),
            interest_level=random.randint(1, 10),
            adviser_group_id=random.choice(adviser_groups).adviser_group_id  # Используем группу советников
        )
        themes.append(theme)
else:
    print("Нет доступных групп научных руководителей для создания тем.")

session.add_all(themes)
session.commit()

# Создание 30 предметов
subjects = []
for _ in range(30):
    subject = Subject(
        subject_name=fake.word()
    )
    subjects.append(subject)

session.add_all(subjects)
session.commit()

# Создание 30 оценок
grades = []
for _ in range(30):
    grade = Grade(
        grade=random.randint( 1, 5)
    )
    grades.append(grade)

session.add_all(grades)
session.commit()

# Создание записей оценок для студентов
grade_records = []
for student in students:
    for _ in range(random.randint(1, 5)):  # Каждому студенту можно дать от 1 до 5 оценок
        grade_record = GradeRecord(
            subject_id=random.choice(subjects).subject_id,
            grade_id=random.choice(grades).grade_id
        )
        grade_records.append(grade_record)

session.add_all(grade_records)
session.commit()

# Создание интересов тем для студентов
student_theme_interests = []
for student in students:
    for _ in range(4):
        student_theme_interest = StudentThemeInterest(
            student_id=student.student_id,
            theme_id=random.choice(themes).theme_id,
            interest_level=random.randint(0, 4)
        )
        student_theme_interests.append(student_theme_interest)

session.add_all(student_theme_interests)
session.commit()

# Создание важности тем для предметов
theme_subject_importances = []
for theme in themes:
    for subject in subjects:
        importance = ThemeSubjectImportance(
            theme_id=theme.theme_id,
            subject_id=subject.subject_id,
            weight=random.uniform(0.1, 1.0)  # Важность от 0.1 до 1.0
        )
        theme_subject_importances.append(importance)

session.add_all(theme_subject_importances)
session.commit()

# Закрытие сессии
session.close()

print("База данных успешно заполнена данными!")