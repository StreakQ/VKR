import unittest
from unittest.mock import MagicMock, patch
from repositories import *

# Предположим, что ваш класс называется DistributionAlgorithmRepository
class TestDistributionAlgorithm(unittest.TestCase):

    @patch('repositories.StudentThemeInterestRepository')
    @patch('repositories.ThemeSubjectImportanceRepository')
    @patch('repositories.AdviserThemeRepository')
    @patch('repositories.DistributionRepository')
    @patch('repositories.StudentSubjectGradeRepository')
    def test_assign_students_to_advisers_and_distribute(self, MockDistributionRepository,
                                                            MockAdviserThemeRepository,
                                                            MockThemeSubjectImportanceRepository,
                                                            MockStudentThemeInterestRepository,
                                                            MockStudentSubjectGradeRepository):
        # Создаем экземпляр класса
        distribution_algorithm = DistributionAlgorithmRepository(
            engine=None,
            student_subject_grade_repository=MockStudentSubjectGradeRepository,
            student_theme_interest_repository=MockStudentThemeInterestRepository,
            theme_subject_importance_repository=MockThemeSubjectImportanceRepository,
            adviser_theme_repository=MockAdviserThemeRepository,
            distribution_repository=MockDistributionRepository
        )

        # Подготовка тестовых данных
        mock_student_interests = [
            MagicMock(student_id=1, theme_id=1, interest_level=5),
            MagicMock(student_id=2, theme_id=2, interest_level=4),
            MagicMock(student_id=3, theme_id=1, interest_level=3),
            MagicMock(student_id=4, theme_id=2, interest_level=1),
        ]

        mock_theme_importance = [
            MagicMock(theme_id=1, subject_id=1, weight=0.5),
            MagicMock(theme_id=2, subject_id=2, weight=0.3),
        ]

        mock_advisers = [
            MagicMock(adviser_id=1, number_of_places=2),
            MagicMock(adviser_id=2, number_of_places=3),
        ]

        # Настройка моков
        MockStudentThemeInterestRepository.Session.return_value.__enter__.return_value.query.return_value.all.return_value = mock_student_interests
        MockThemeSubjectImportanceRepository.Session.return_value.__enter__.return_value.query.return_value.all.return_value = mock_theme_importance
        MockAdviserThemeRepository.Session.return_value.__enter__.return_value.query.return_value.all.return_value = mock_advisers

        # Выполнение функции
        unassigned_students = distribution_algorithm.assign_students_to_advisers_and_distribute()

        # Проверка результатов
        self.assertEqual(len(unassigned_students), 1)  # Ожидаем, что один студент не будет назначен
        self.assertIn(3, unassigned_students)  # Проверяем, что студент с ID 3 не назначен

        # Проверка, что распределение было добавлено
        MockDistributionRepository.add_distribution.assert_called_once()

if __name__ == '__main__':
    unittest.main()

#TODO 1: разобраться либо с моками либо с самой функцией распределения