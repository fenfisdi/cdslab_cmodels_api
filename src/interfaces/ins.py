from src.models.db.ins import INSVariable


class INSInterface:

    @staticmethod
    def find_all():
        return INSVariable.objects().all()

    @staticmethod
    def find_one(representation: str) -> INSVariable:
        filters = {
            'representation': representation,
        }
        return INSVariable.objects(**filters).first()
