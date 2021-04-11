from src.db import get_db_connection


def model_db():
    return get_db_connection().get_collection('cmodels')
