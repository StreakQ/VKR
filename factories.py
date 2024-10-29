from sqlalchemy import create_engine
from models import Base
from repositories import *

class RepositoryFactory:
    @staticmethod
    def create_student_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentRepository(engine)

    @staticmethod
    def create_adviser_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return AdviserRepository(engine)

    @staticmethod
    def create_subject_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return SubjectRepository(engine)

    @staticmethod
    def create_theme_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return ThemeRepository(engine)

    @staticmethod
    def create_grade_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return GradeRepository(engine)

    @staticmethod
    def create_grade_record_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return GradeRecordRepository(engine)

    @staticmethod
    def create_student_grade_record_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentGradeRecordRepository(engine)

    @staticmethod
    def create_student_theme_interest_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentThemeInterestRepository(engine)

    @staticmethod
    def create_theme_subject_importance_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return ThemeSubjectImportanceRepository(engine)

    @staticmethod
    def create_adviser_group_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return AdviserGroupRepository(engine)

    @staticmethod
    def create_distribution_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)

        # Создание зависимых репозиториев
        student_grade_record_repo = RepositoryFactory.create_student_grade_record_repository(db_url)
        student_theme_interest_repo = RepositoryFactory.create_student_theme_interest_repository(db_url)
        theme_subject_importance_repo = RepositoryFactory.create_theme_subject_importance_repository(db_url)

        # Возвращаем DistributionRepository с зависимыми репозиториями
        return DistributionRepository(engine, student_grade_record_repo, student_theme_interest_repo,
                                      theme_subject_importance_repo)