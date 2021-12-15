from src.interfaces import INSInterface
from src.models.db import INSVariable


class CreatePredefinedINS:

    @classmethod
    def handle(cls):
        predefined = {
            'I': 'Infected',
            'R': 'Recovered',
        }

        for k, v in predefined.items():
            variable_found = INSInterface.find_one(representation=k)
            if not variable_found:
                new_variable = INSVariable(
                    label=v,
                    representation=k,
                )
                try:
                    new_variable.save()
                finally:
                    new_variable.reload()
