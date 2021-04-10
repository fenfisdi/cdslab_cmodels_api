from bson.objectid import ObjectId

from src.db import get_db_connection


def simulation_db():
    return get_db_connection().get_collection('cmodels_simulation')