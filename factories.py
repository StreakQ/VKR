
from sqlalchemy import create_engine
from models import Base
from repositories import (
    StudentRepository,
    AdviserRepository,
    SubjectRepository,
    ThemeRepository,
    AdviserThemeRepository,
    StudentSubjectGradeRepository,
    StudentThemeInterestRepository,
    ThemeSubjectImportanceRepository,
    DistributionRepository,
    DistributionAlgorithmRepository
)

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
    def create_adviser_theme_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return AdviserThemeRepository(engine, adviser_repository=AdviserRepository, theme_repository=ThemeRepository)

    @staticmethod
    def create_student_subject_grade_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentSubjectGradeRepository(engine,student_repository=StudentRepository,subject_repository=SubjectRepository)

    @staticmethod
    def create_student_theme_interest_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentThemeInterestRepository(engine, student_repository=StudentRepository,theme_repository=ThemeRepository)

    @staticmethod
    def create_theme_subject_importance_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return ThemeSubjectImportanceRepository(engine, theme_repository=ThemeRepository,subject_repository=SubjectRepository)

    @staticmethod
    def create_distribution_algorithm_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return DistributionAlgorithmRepository(engine,
                                      distribution_repository=DistributionRepository,
                                      student_subject_grade_repository=StudentSubjectGradeRepository,
                                      student_theme_interest_repository= StudentThemeInterestRepository,
                                      theme_subject_importance_repository= ThemeSubjectImportanceRepository,
                                      adviser_theme_repository=AdviserThemeRepository
                                      )

    @staticmethod
    def create_distribution_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return DistributionRepository(engine)

