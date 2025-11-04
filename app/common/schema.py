from pydantic import BaseModel
import re
import string
from datetime import timedelta


class SchemaBase(BaseModel):

    @classmethod
    def to_dict(cls):
        return {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith('__') and not callable(v)
        }


class Validate:

    @staticmethod
    def phone(value: str):
        if not re.match(r'^((\+7)([0-9]){10})$', value):
            raise ValueError(
                'Unsupported phone type. Allowed syntax is +7xxxxxxxxxx, '
                'where x is a digit 0..9'
            )
        return value

    @staticmethod
    def password(value: str):
        has_lower_letter = any(c in string.ascii_lowercase for c in value)
        has_upper_letter = any(c in string.ascii_uppercase for c in value)
        has_digits = any(c in string.digits for c in value)
        has_special_symbols = any(c in string.punctuation for c in value)

        if not has_digits:
            raise ValueError('use digits in your password.')
        if not has_upper_letter:
            raise ValueError('use uppercase letters in your password.')
        if not has_lower_letter:
            raise ValueError('use lowercase letters in your password.')
        if not has_special_symbols:
            raise ValueError(f'use special symbols in your password ({
                string.punctuation
            }).')

        return value

    @staticmethod
    def dates_range(
        cls_proxy,
        date_before,
        date_after,
        min_delta=timedelta(days=1),
        max_delta=timedelta(days=356),
        msg_on_error='dates are incorrect'
    ):
        if min_delta <= date_after - date_before <= max_delta:
            return cls_proxy
        raise ValueError(msg_on_error)

