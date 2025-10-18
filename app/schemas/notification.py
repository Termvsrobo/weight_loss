from pydantic import BaseModel, ConfigDict


class PreferenceSchema(BaseModel):
    motivation: bool = False
    reminders: bool = False
    accruals: bool = False

    model_config = ConfigDict(from_attributes=True)
