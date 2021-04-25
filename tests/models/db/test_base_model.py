from pydantic import ValidationError
import pytest

from src.models.db.base_model import MetadataBaseDoc


def test_SimulationConfig():
    try:
        MetadataBaseDoc(id='not a bson.ObjectID')
    except ValidationError:
        assert True
    else:
        assert pytest.fail('MetadataBaseDoc must contain id field')
