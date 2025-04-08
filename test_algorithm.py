import unittest
from unittest.mock import MagicMock
from repositories import *
import logging

logging.basicConfig(level=logging.DEBUG)

class TestAlgorithm(unittest.TestCase):

    def setUp(self):
        """
        Подготовка моков для теста.
        """
        # Моки для репозиториев
        self.mock_student_theme_interest_repository = MagicMock()
        self.mock_student_theme_interest_repository.get_all.return_value = [
            {"student_id": 1, "theme_id": 5, "interest_level": 3},
            {"student_id": 2, "theme_id": 7, "interest_level": 4},
        ]

        self.mock_student_subject_grade_repository = MagicMock()
        self.mock_student_subject_grade_repository.get_all.return_value = [
            {"student_id": 1, "subject_id": 1, "grade": 5},
            {"student_id": 2, "subject_id": 2, "grade": 4},
        ]

        self.mock_theme_subject_importance_repository = MagicMock()
        self.mock_theme_subject_importance_repository.get_all.return_value = [
            {"theme_id": 5, "subject_id": 1, "weight": 0.8},
            {"theme_id": 7, "subject_id": 2, "weight": 0.6},
        ]

        self.mock_adviser_theme_repository = MagicMock()
        self.mock_adviser_theme_repository.get_all.return_value = [
            {"adviser_id": 1, "theme_id": 5},
            {"adviser_id": 2, "theme_id": 7},
        ]

        self.mock_distribution_repository = MagicMock()

        # Создание мокированной сессии
        self.mock_session = MagicMock()
        self.mock_engine = MagicMock()
        self.mock_engine.sessionmaker.return_value = self.mock_session

        # Настройка данных для запросов
        self.mock_session.query.side_effect = lambda model: {
            Adviser: MagicMock(all=MagicMock(return_value=[
                {"adviser_id": 1, "number_of_places": 2},
                {"adviser_id": 2, "number_of_places": 3}
            ])),
            Theme: MagicMock(all=MagicMock(return_value=[
                {"theme_id": 5, "title": "Тема 1"},
                {"theme_id": 7, "title": "Тема 2"}
            ])),
            Student: MagicMock(all=MagicMock(return_value=[
                {"student_id": 1, "name": "Иван"},
                {"student_id": 2, "name": "Анна"}
            ]))
        }[model]
        self.mock_session.add.side_effect = lambda obj: None
        self.mock_session.commit.side_effect = lambda: None

        # Создание экземпляра класса
        self.distribution_algorithm = DistributionAlgorithmRepository(
            engine=self.mock_engine,
            student_subject_grade_repository=self.mock_student_subject_grade_repository,
            theme_subject_importance_repository=self.mock_theme_subject_importance_repository,
            adviser_theme_repository=self.mock_adviser_theme_repository,
            student_theme_interest_repository=self.mock_student_theme_interest_repository,
            distribution_repository=self.mock_distribution_repository
        )

    def test_assign_students_to_adviser_and_distribute(self):
        """
        Тестирование алгоритма распределения студентов.
        """
        # Выполнение метода
        unassigned_students = self.distribution_algorithm.assign_students_to_advisers_and_distribute()

        # Проверка результатов
        self.assertEqual(len(unassigned_students), 0)
        self.mock_distribution_repository.add_distribution.assert_called_once()
        logging.debug("Неназначенные студенты:")
        for student in unassigned_students:
            logging.debug(f"Студент ID: {student['student_id']}")


    def test_distribution_with_one_unavailable_adviser(self):
        """
        Тестирование алгоритма распределения, когда один научный руководитель недоступен.
        """
        # Настройка данных для научных руководителей
        mock_advisers = [
            {"adviser_id": 1, "number_of_places": 0},
            {"adviser_id": 2, "number_of_places": 3}
        ]
        self.mock_session.query.side_effect = lambda model: {
            Adviser: MagicMock(all=MagicMock(return_value=mock_advisers)),
            Theme: MagicMock(all=MagicMock(return_value=[
                {"theme_id": 5, "title": "Тема 1"},
                {"theme_id": 7, "title": "Тема 2"}
            ])),
            Student: MagicMock(all=MagicMock(return_value=[
                {"student_id": 1, "name": "Иван"},
                {"student_id": 2, "name": "Анна"}
            ]))
        }[model]

        # Выполнение метода
        unassigned_students = self.distribution_algorithm.assign_students_to_advisers_and_distribute()
        self.assertEqual(len(unassigned_students), 0)  # Все студенты должны быть назначены
        self.mock_distribution_repository.add_distribution.assert_called_once()
        logging.debug("Неназначенные студенты:")
        for student in unassigned_students:
            logging.debug(f"Студент ID: {student['student_id']}")


import unittest
from unittest.mock import MagicMock
from repositories import *
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


class TestAlgorithm(unittest.TestCase):

    def setUp(self):
        """
        Подготовка моков для теста.
        """
        # Моки для репозиториев
        self.mock_student_theme_interest_repository = MagicMock()
        self.mock_adviser_theme_repository = MagicMock()
        self.mock_distribution_repository = MagicMock()
        self.mock_student_subject_grade_repository = MagicMock()  # Новый мок
        self.mock_theme_subject_importance_repository = MagicMock()  # Новый мок

        # Создание мокированной сессии
        self.mock_session = MagicMock()
        self.mock_engine = MagicMock()
        self.mock_engine.sessionmaker.return_value = self.mock_session

        # Настройка данных для запросов
        self.mock_session.query.side_effect = lambda model: {
            Adviser: MagicMock(all=MagicMock(return_value=[
                {"adviser_id": 1, "number_of_places": 1},
                {"adviser_id": 2, "number_of_places": 1},
                {"adviser_id": 3, "number_of_places": 1},
                {"adviser_id": 4, "number_of_places": 1},
                {"adviser_id": 5, "number_of_places": 1},
                {"adviser_id": 6, "number_of_places": 1}
            ])),
            Theme: MagicMock(all=MagicMock(return_value=[
                {"theme_id": 101, "title": "Тема 1"},
                {"theme_id": 102, "title": "Тема 2"},
                {"theme_id": 103, "title": "Тема 3"},
                {"theme_id": 104, "title": "Тема 4"},
                {"theme_id": 105, "title": "Тема 5"},
                {"theme_id": 106, "title": "Тема 6"}
            ])),
            Student: MagicMock(all=MagicMock(return_value=[
                {"student_id": 1, "name": "Иван"},
                {"student_id": 2, "name": "Анна"},
                {"student_id": 3, "name": "Петр"},
                {"student_id": 4, "name": "Мария"},
                {"student_id": 5, "name": "Сергей"}
            ]))
        }[model]

        # Настройка данных для интересов студентов
        self.mock_student_theme_interest_repository.get_all.return_value = [
            {"student_id": 1, "theme_id": 101, "interest_level": 1},
            {"student_id": 2, "theme_id": 101, "interest_level": 1},
            {"student_id": 3, "theme_id": 101, "interest_level": 1},
            {"student_id": 4, "theme_id": 101, "interest_level": 1},
            {"student_id": 5, "theme_id": 101, "interest_level": 1},
            {"student_id": 1, "theme_id": 102, "interest_level": 2},
            {"student_id": 2, "theme_id": 103, "interest_level": 2},
            {"student_id": 3, "theme_id": 104, "interest_level": 2},
            {"student_id": 4, "theme_id": 105, "interest_level": 2},
            {"student_id": 5, "theme_id": 106, "interest_level": 2},
        ]

        # Настройка данных для назначений тем научным руководителям
        self.mock_adviser_theme_repository.get_all.return_value = [
            {"adviser_id": 1, "theme_id": 101},
            {"adviser_id": 2, "theme_id": 102},
            {"adviser_id": 3, "theme_id": 103},
            {"adviser_id": 4, "theme_id": 104},
            {"adviser_id": 5, "theme_id": 105},
            {"adviser_id": 6, "theme_id": 106}
        ]

        # Создание экземпляра класса
        self.distribution_algorithm = DistributionAlgorithmRepository(
            engine=self.mock_engine,
            student_theme_interest_repository=self.mock_student_theme_interest_repository,
            adviser_theme_repository=self.mock_adviser_theme_repository,
            distribution_repository=self.mock_distribution_repository,
            student_subject_grade_repository=self.mock_student_subject_grade_repository,  # Добавлено
            theme_subject_importance_repository=self.mock_theme_subject_importance_repository  # Добавлено
        )

    def test_redistribution_when_all_students_want_the_same_theme(self):
        """
        Тестирование алгоритма перераспределения студентов, когда все хотят одну и ту же тему.
        """
        # Выполнение метода
        unassigned_students = self.distribution_algorithm.assign_students_to_advisers_and_distribute()

        # Проверка результатов
        self.assertEqual(len(unassigned_students), 0)  # Все студенты должны быть назначены
        self.mock_distribution_repository.add_distribution.assert_called()  # Проверяем, что данные сохранялись

        # Логирование финального состояния научных руководителей
        logging.debug("Финальное состояние научных руководителей:")
        for adviser_id, places in self.distribution_algorithm.advisers.items():
            logging.debug(f"ID Руководителя: {adviser_id}, Оставшиеся места: {places.number_of_places}")

        # Логирование распределенных студентов
        logging.debug("Распределенные студенты:")
        for call in self.mock_distribution_repository.add_distribution.call_args_list:
            distributions = call.args[0]
            for distribution in distributions:
                student_id = distribution["student_id"]
                theme_id = distribution["theme_id"]
                adviser_id = distribution["adviser_id"]

                # Логируем назначение студента
                logging.info(
                    f"Студент ID: {student_id} назначен Научному руководителю ID: {adviser_id}, "
                    f"Тема ID: {theme_id}"
                )

        # Проверяем, что каждый научный руководитель получил только одного студента
        assigned_advisers = {}
        for call in self.mock_distribution_repository.add_distribution.call_args_list:
            distributions = call.args[0]
            for distribution in distributions:
                adviser_id = distribution["adviser_id"]
                if adviser_id not in assigned_advisers:
                    assigned_advisers[adviser_id] = 0
                assigned_advisers[adviser_id] += 1

        for adviser_id, count in assigned_advisers.items():
            self.assertLessEqual(count, 1, f"Научный руководитель ID {adviser_id} получил больше 1 студента")

        # Проверяем, что студенты были переназначены на темы с более низким уровнем интереса
        for call in self.mock_distribution_repository.add_distribution.call_args_list:
            distributions = call.args[0]
            for distribution in distributions:
                student_id = distribution["student_id"]
                theme_id = distribution["theme_id"]
                interest_level = next(
                    (item["interest_level"] for item in self.mock_student_theme_interest_repository.get_all.return_value
                     if item["student_id"] == student_id and item["theme_id"] == theme_id),
                    None
                )
                self.assertIsNotNone(interest_level, f"Не найден уровень интереса для студента {student_id}")
                logging.debug(f"Студент ID: {student_id}, Тема ID: {theme_id}, Уровень интереса: {interest_level}")


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()