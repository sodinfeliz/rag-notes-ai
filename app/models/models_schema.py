from pydantic import BaseModel, Field


class ModelsResponse(BaseModel):
    models: list[str] = Field(..., description="List of available model names")
    platforms: list[str] = Field(..., description="Corresponding platform for each model")
    errors: dict[str, str] | None = Field(None, description="Errors from model sources, if any")
