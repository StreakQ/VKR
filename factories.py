from sqlalchemy import create_engine
from models import Base
from repositories import StudentRepository

class RepositoryFactory:
    @staticmethod
    def create_student_repository(db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        return StudentRepository(engine)