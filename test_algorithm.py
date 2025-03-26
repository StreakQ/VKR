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




if __name__ == '__main__':
    unittest.main()