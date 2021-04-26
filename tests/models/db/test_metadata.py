from pydantic import ValidationError
import pytest

from src.models.db.metadata import MetadataBaseDoc


def test_SimulationConfig():
    with pytest.raises(ValidationError):
        MetadataBaseDoc(id='not a bson.ObjectID')
