import inspect
import re
import string
from copy import deepcopy
from datetime import timedelta
from typing import Annotated, Any, List, Optional, Tuple, Type

from fastapi import Form
from pydantic import BaseModel, create_model, model_validator
from pydantic.fields import FieldInfo

from app.entities.common.exc import InvalidRequest


@model_validator(mode="after")
def validate_at_least_one_unrequired(self: BaseModel):
    required_fields = ["id"]
    filled_fields = [
        field_name
        for field_name, field_value in self.model_dump(exclude_none=True).items()
        if field_name not in required_fields and field_value is not None
    ]
    if len(filled_fields) < 1:
        raise InvalidRequest(
            detail="Not enough unrequired fields filled in request body"
        )
    return self


def partial_model(required_fields: List[str] | None = None):
    if required_fields is None:
        required_fields = []

    def wrapper(model: Type[BaseModel]) -> Type[BaseModel]:
        def make_field_optional(
            field: FieldInfo, default: Any = None
        ) -> Tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]  # type: ignore
            return new.annotation, new

        create_model_alias: Any = create_model  # to ignore linters warning
        partial_model_class = create_model_alias(
            f"Partial{model.__name__}",
            __base__=model,
            __module__=model.__module__,
            __validators__={
                "validate_number_of_unrequired_fields": validate_at_least_one_unrequired
            },
            **{
                field_name: make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()
                if field_name not in required_fields
            },
        )
        return partial_model_class

    return wrapper


class SchemaBase(BaseModel):

    @classmethod
    def to_dict(cls):
        return {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith("__") and not callable(v)
        }


class Validate:

    @staticmethod
    def phone(value: str):
        if not re.match(r"^((\+7)([0-9]){10})$", value):
            raise ValueError(
                "Unsupported phone type. Allowed syntax is +7xxxxxxxxxx, "
                "where x is a digit 0..9"
            )
        return value

    @staticmethod
    def password(value: str):
        has_lower_letter = any(c in string.ascii_lowercase for c in value)
        has_upper_letter = any(c in string.ascii_uppercase for c in value)
        has_digits = any(c in string.digits for c in value)
        has_special_symbols = any(c in string.punctuation for c in value)

        if not has_digits:
            raise ValueError("use digits in your password.")
        if not has_upper_letter:
            raise ValueError("use uppercase letters in your password.")
        if not has_lower_letter:
            raise ValueError("use lowercase letters in your password.")
        if not has_special_symbols:
            raise ValueError(
                f"use special symbols in your password ({string.punctuation})."
            )

        return value

    @staticmethod
    def dates_range(
        cls_proxy,
        date_before,
        date_after,
        min_delta=timedelta(days=1),
        max_delta=timedelta(days=356),
        msg_on_error="dates are incorrect",
    ):
        if min_delta <= date_after - date_before <= max_delta:
            return cls_proxy
        raise ValueError(msg_on_error)


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, *model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls
    return cls
