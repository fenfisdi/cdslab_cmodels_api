from uuid import uuid1, UUID


class IdentifierUseCase:

    @classmethod
    def create_identifier(cls) -> UUID:
        """
        Create a new id
        """
        return uuid1()
