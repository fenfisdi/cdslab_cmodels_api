class CmodelUseCases:

    @staticmethod
    def model_information_in_db_to_compare(model_in_db: dict) -> dict:
        model_in_db.pop('_id')
        model_in_db.pop('inserted_at')
        model_in_db.pop('updated_at')
        return model_in_db
