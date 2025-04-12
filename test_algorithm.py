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
        self.mock_student_theme_interest_repository = MagicMock()
        self.mock_adviser_theme_repository = MagicMock()
        self.mock_distribution_repository = MagicMock()
        self.mock_student_subject_grade_repository = MagicMock()
        self.mock_theme_subject_importance_repository = MagicMock()

        # Мокированные данные для интересов студентов
        self.mock_student_theme_interest_repository.get_all.return_value = [
            {"student_id": 1, "theme_id": 1, "interest_level": 1},  # Все студенты хотят одну и ту же тему
            {"student_id": 2, "theme_id": 1, "interest_level": 1},
            {"student_id": 3, "theme_id": 1, "interest_level": 1},
            {"student_id": 4, "theme_id": 1, "interest_level": 1},
            {"student_id": 5, "theme_id": 1, "interest_level": 1},
            {"student_id": 1, "theme_id": 2, "interest_level": 2},  # Уникальная тема для второго руководителя
            {"student_id": 2, "theme_id": 3, "interest_level": 3},  # Уникальная тема для третьего руководителя
            {"student_id": 3, "theme_id": 4, "interest_level": 4},  # Уникальная тема для четвертого руководителя
            {"student_id": 4, "theme_id": 5, "interest_level": 5},  # Уникальная тема для пятого руководителя
            {"student_id": 5, "theme_id": 6, "interest_level": 5},  # Уникальная тема для шестого руководителя
        ]
        logging.debug("Мокированные данные для интересов студентов успешно настроены.")

        # Мокированные данные для связей научных руководителей и тем
        self.mock_adviser_theme_repository.get_all.return_value = [
            {"adviser_id": 1, "theme_id": 1},  # Первый руководитель имеет только одну тему
            {"adviser_id": 2, "theme_id": 2},  # Второй руководитель имеет уникальную тему
            {"adviser_id": 3, "theme_id": 3},  # Третий руководитель имеет уникальную тему
            {"adviser_id": 4, "theme_id": 4},  # Четвертый руководитель имеет уникальную тему
            {"adviser_id": 5, "theme_id": 5},  # Пятый руководитель имеет уникальную тему
            {"adviser_id": 6, "theme_id": 6},  # Шестой руководитель имеет уникальную тему
        ]
        logging.debug("Мокированные данные для связей научных руководителей и тем успешно настроены.")

        # Мокированные данные для научных руководителей
        self.mock_adviser_repository = MagicMock()
        self.mock_adviser_repository.get_all.return_value = [
            {"adviser_id": 1, "number_of_places": 1},  # У первого руководителя только одно место
            {"adviser_id": 2, "number_of_places": 1},
            {"adviser_id": 3, "number_of_places": 1},
            {"adviser_id": 4, "number_of_places": 1},
            {"adviser_id": 5, "number_of_places": 1},
            {"adviser_id": 6, "number_of_places": 1},
        ]
        logging.debug("Мокированные данные для научных руководителей успешно настроены.")

        # Создание экземпляра класса DistributionAlgorithmRepository
        self.distribution_algorithm = DistributionAlgorithmRepository(
            engine=MagicMock(),
            student_theme_interest_repository=self.mock_student_theme_interest_repository,
            adviser_theme_repository=self.mock_adviser_theme_repository,
            distribution_repository=self.mock_distribution_repository,
            student_subject_grade_repository=self.mock_student_subject_grade_repository,
            theme_subject_importance_repository=self.mock_theme_subject_importance_repository
        )
        logging.debug("Экземпляр DistributionAlgorithmRepository успешно создан.")

    def test_redistribution_when_all_students_want_the_same_theme(self):
        """
        Тестирование алгоритма перераспределения студентов,
        когда все хотят одну и ту же тему, но у первого руководителя ограниченное количество мест.
        """
        logging.info("Запуск теста: test_redistribution_when_all_students_want_the_same_theme")

        try:
            # Логирование начального состояния
            logging.debug("Начальное состояние:")
            logging.debug(f"Интересы студентов: {self.mock_student_theme_interest_repository.get_all.return_value}")
            logging.debug(
                f"Связи научных руководителей и тем: {self.mock_adviser_theme_repository.get_all.return_value}")
            logging.debug(f"Научные руководители: {self.mock_adviser_repository.get_all.return_value}")

            # Выполнение метода распределения
            logging.debug("Выполнение метода assign_students_to_advisers_and_distribute...")
            unassigned_students = self.distribution_algorithm.assign_students_to_advisers_and_distribute()
            logging.debug("Метод assign_students_to_advisers_and_distribute завершен.")

            # Проверка, что все студенты были назначены
            logging.debug(f"Количество неназначенных студентов: {len(unassigned_students)}")
            self.assertEqual(len(unassigned_students), 0, "Не все студенты были назначены.")
            logging.debug("Все студенты успешно назначены.")

            # Проверка, что метод add_distribution был вызван
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

            logging.info("Тест успешно завершен.")

        except Exception as e:
            logging.error(f"Ошибка при выполнении теста: {e}")
            raise


if __name__ == "__main__":
    unittest.main()