import re
from pydantic import BaseModel, EmailStr, field_validator
from constants.ddds_brazil import DDDS_BRASIL

PHONE_REGEX = r'^(\+55)?(\(\d{2}\)|\d{2})(\d{4,5})[-]?(\d{4})$'

class Lead(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator('phone')
    def validator_digit_brazil(cls, v):
        if not re.match(PHONE_REGEX, v):
            raise ValueError("Formato de telefone inválido.")

        digits = re.sub(r'\D', '', v)

        if digits.startswith("55"):
            digits = digits[2:]

        ddd = digits[:2]
        if ddd not in DDDS_BRASIL:
            raise ValueError("DDD inválido.")

        return digits
