import unittest
from unittest.mock import MagicMock
from repositories import *
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        """
        Подготовка моков для теста.
        """
        logging.debug("Инициализация тестового окружения...")

        # Моки для репозиториев
        self.mock_distribution_repository = MagicMock()  # Для сохранения распределений
        self.mock_student_grade_record_repository = MagicMock()  # Оценки студентов по предметам
        self.mock_student_theme_interest_repository = MagicMock()  # Интересы студентов к темам
        self.mock_theme_subject_importance_repository = MagicMock()  # Важность тем для предметов
        self.mock_adviser_theme_repository = MagicMock()  # Связи научных руководителей и тем

        # Мокированные данные для интересов студентов
        self.mock_student_theme_interest_repository.get_all.return_value = [
            {"student_id": 1, "theme_id": 1, "interest_level": 1},  # Первый студент интересуется темой 1 (уровень 1)
            {"student_id": 1, "theme_id": 2, "interest_level": 2},  # Первый студент интересуется темой 2 (уровень 2)
            {"student_id": 2, "theme_id": 1, "interest_level": 1},  # Второй студент интересуется темой 1 (уровень 1)
            {"student_id": 2, "theme_id": 3, "interest_level": 2},  # Второй студент интересуется темой 3 (уровень 2)
            {"student_id": 3, "theme_id": 1, "interest_level": 1},  # Третий студент интересуется темой 1 (уровень 1)
            {"student_id": 3, "theme_id": 4, "interest_level": 2},  # Третий студент интересуется темой 4 (уровень 2)
        ]
        logging.debug("Мокированные данные для интересов студентов успешно настроены.")

        # Мокированные данные для связей научных руководителей и тем
        self.mock_adviser_theme_repository.get_all.return_value = [
            {"adviser_id": 1, "theme_id": 1},
            {"adviser_id": 2, "theme_id": 2},
            {"adviser_id": 3, "theme_id": 3},
            {"adviser_id": 4, "theme_id": 4},
        ]
        logging.debug("Мокированные данные для связей научных руководителей и тем успешно настроены.")

        # Мокированные данные для оценок студентов по предметам
        self.mock_student_grade_record_repository.get_all.return_value = [
            {"student_id": 1, "subject_id": 1, "grade": 5},
            {"student_id": 1, "subject_id": 2, "grade": 4},
            {"student_id": 2, "subject_id": 1, "grade": 4},
            {"student_id": 2, "subject_id": 2, "grade": 5},
            {"student_id": 3, "subject_id": 1, "grade": 3},
            {"student_id": 3, "subject_id": 2, "grade": 4},
        ]
        logging.debug("Мокированные данные для оценок студентов по предметам успешно настроены.")

        # Мокированные данные для важности тем для предметов
        self.mock_theme_subject_importance_repository.get_all.return_value = [
            {"theme_id": 1, "subject_id": 1, "weight": 0.8},
            {"theme_id": 1, "subject_id": 2, "weight": 0.2},
            {"theme_id": 2, "subject_id": 1, "weight": 0.7},
            {"theme_id": 2, "subject_id": 2, "weight": 0.3},
            {"theme_id": 3, "subject_id": 1, "weight": 0.6},
            {"theme_id": 3, "subject_id": 2, "weight": 0.4},
            {"theme_id": 4, "subject_id": 1, "weight": 0.5},
            {"theme_id": 4, "subject_id": 2, "weight": 0.5},
        ]
        logging.debug("Мокированные данные для важности тем успешно настроены.")

        # Создание экземпляра класса DistributionAlgorithmRepository
        self.distribution_algorithm = DistributionAlgorithmRepository(
            engine=MagicMock(),
            student_subject_grade_repository=self.mock_student_grade_record_repository,
            student_theme_interest_repository=self.mock_student_theme_interest_repository,
            theme_subject_importance_repository=self.mock_theme_subject_importance_repository,
            adviser_theme_repository=self.mock_adviser_theme_repository,
            distribution_repository=self.mock_distribution_repository
        )
        logging.debug("Экземпляр DistributionAlgorithmRepository успешно создан.")

    def test_replacement_mechanism(self):
        """
        Тестирование механизма переназначения студентов.
        Проверяется, что на тему назначается самый подходящий студент,
        даже если туда уже был кто-то назначен.
        """
        logging.info("Запуск теста: test_replacement_mechanism")

        try:
            # Логирование начального состояния
            logging.debug("Начальное состояние:")
            logging.debug(f"Интересы студентов: {self.mock_student_theme_interest_repository.get_all.return_value}")
            logging.debug(f"Оценки студентов: {self.mock_student_grade_record_repository.get_all.return_value}")
            logging.debug(f"Веса тем: {self.mock_theme_subject_importance_repository.get_all.return_value}")
            logging.debug(
                f"Связи научных руководителей и тем: {self.mock_adviser_theme_repository.get_all.return_value}"
            )

            # Выполнение метода распределения
            logging.debug("Выполнение метода assign_students_to_advisers_and_distribute...")
            unassigned_students = self.distribution_algorithm.assign_students_to_advisers_and_distribute()
            logging.debug("Метод assign_students_to_advisers_and_distribute завершен.")

            # Проверка, что все студенты были назначены
            logging.debug(f"Количество неназначенных студентов: {len(unassigned_students)}")
            self.assertEqual(len(unassigned_students), 0, "Не все студенты были назначены.")
            logging.debug("Все студенты успешно назначены.")

            # Проверка вызова метода add_distribution
            logging.debug("Проверка вызова метода add_distribution...")
            self.mock_distribution_repository.add_distribution.assert_called()
            logging.debug("Метод add_distribution был вызван.")

            # Логирование данных, переданных в add_distribution
            final_distribution = []
            for call in self.mock_distribution_repository.add_distribution.call_args_list:
                distributions = call.args[0]
                logging.debug(f"Данные, переданные в add_distribution: {distributions}")

                for distribution in distributions:
                    student_id = distribution["student_id"]
                    theme_id = distribution["theme_id"]
                    adviser_id = distribution["adviser_id"]

                    # Получаем уровень интереса студента к назначенной теме
                    interest_level = next(
                        (
                            item["interest_level"]
                            for item in self.mock_student_theme_interest_repository.get_all.return_value
                            if item["student_id"] == student_id and item["theme_id"] == theme_id
                        ),
                        None,
                    )
                    final_distribution.append({
                        "student_id": student_id,
                        "adviser_id": adviser_id,
                        "theme_id": theme_id,
                        "interest_level": interest_level
                    })

            # Логирование собранных данных
            logging.debug(f"Собранные данные о распределении: {final_distribution}")

            # Отображение финального распределения
            logging.info("Финальное распределение студентов:")
            logging.info("{:<10} {:<15} {:<10} {:<15}".format("Student ID", "Adviser ID", "Theme ID", "Interest Level"))
            logging.info("-" * 50)
            for record in final_distribution:
                logging.info("{:<10} {:<15} {:<10} {:<15}".format(
                    record["student_id"],
                    record["adviser_id"],
                    record["theme_id"],
                    record["interest_level"]
                ))

            # Проверка, что на тему назначен самый подходящий студент
            logging.debug("Проверка механизма переназначения...")
            assigned_students_per_theme = {}
            for record in final_distribution:
                theme_id = record["theme_id"]
                student_id = record["student_id"]
                interest_level = record["interest_level"]

                if theme_id not in assigned_students_per_theme:
                    assigned_students_per_theme[theme_id] = []

                assigned_students_per_theme[theme_id].append((student_id, interest_level))

            # Проверяем, что на каждую тему назначен студент с максимальным уровнем интереса
            for theme_id, students in assigned_students_per_theme.items():
                logging.debug(f"Тема ID: {theme_id}, Назначенные студенты: {students}")
                best_student = max(students, key=lambda x: x[1])  # Студент с максимальным уровнем интереса
                logging.debug(f"Лучший студент для Темы ID: {theme_id}: {best_student}")

                # Проверяем, что только один студент назначен на тему
                self.assertEqual(len(students), 1, f"На Тему ID: {theme_id} назначено больше одного студента.")
                self.assertEqual(students[0], best_student, f"На Тему ID: {theme_id} назначен не самый подходящий студент.")

            logging.info("Тест успешно завершен.")

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {e}")
            raise


if __name__ == "__main__":
    unittest.main()