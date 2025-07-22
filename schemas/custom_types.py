from pydantic import BaseModel, field_validator
from typing import Annotated
from annotated_types import Predicate
import re

PHONE_REGEX = re.compile(r"/^\+?[1-9]\d{1,14}$")

phone_number = Annotated[
    str,
    Predicate(lambda x: bool(PHONE_REGEX.fullmatch(x))),
    "Must be a valid international phone number"
]