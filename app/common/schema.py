from pydantic import BaseModel


class SchemaBase(BaseModel):

    @classmethod
    def to_dict(cls):
        return {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith('__') and not callable(v)
        }
