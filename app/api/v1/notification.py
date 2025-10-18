from pathlib import Path

from fastapi import APIRouter, Request

from models.notification import PreferenceModel
from schemas.notification import PreferenceSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_preferences")
async def get_preferences(request: Request) -> PreferenceSchema:
    preference = PreferenceModel.filter(user_id=request.state.user.id).first()
    if preference:
        preference_model = PreferenceSchema.model_validate(preference)
    else:
        preference_model = PreferenceSchema()
    return preference_model


@router.post("/set_preferences")
async def set_preferences(request: Request, new_preference: PreferenceSchema):
    preference = PreferenceModel.filter(user_id=request.state.user.id).first()
    if preference:
        PreferenceModel.update(new_preference.model_dump(), id=preference.id)
        preference.refresh_from_db()
    else:
        preference = PreferenceModel(
            user_id=request.state.user.id,
            **new_preference.model_dump()
        )
        preference.save()
    return PreferenceSchema.model_validate(preference)
