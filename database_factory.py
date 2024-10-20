from sqlite_database import SQLiteDatabase

class DatabaseFactory:
    @staticmethod
    def create_database(database_type, database):
        if database_type == 'sqlite':
            return SQLiteDatabase(database)
        else:
            raise ValueError('Неподдерживаемый тип базы данных')