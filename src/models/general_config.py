from bson.objectid import ObjectId as BsonObjectId


class GeneralConfig:
    allow_population_by_field_name = True
    extra = 'forbid'


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return v
