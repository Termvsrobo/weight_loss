from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class PhoneMixin:
    phone: PhoneNumber

    def __init__(self, **data):
        if "phone" in data and data["phone"]:
            if data["phone"].startswith("8"):
                data["phone"] = f"+7{data['phone'][1:]}"
            for sym in ("-", " ", "(", ")"):
                data["phone"] = data["phone"].replace(sym, "")
        super().__init__(**data)


class PhoneModel(PhoneMixin, BaseModel): ...


class UserModel(BaseModel): ...
