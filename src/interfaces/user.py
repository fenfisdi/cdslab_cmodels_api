from src.models.db.user import User


class UserInterface:
    '''
        Class to query the user db
    '''

    @staticmethod
    def find_one(email: str) -> User:
        '''
            Search the database for the user corresponding to the email
        Parameter:
            email (str): user email.
        Return:
            User: corresponding user information
        '''

        filters = dict(
            email=email
        )
        return User.objects(**filters).first()
