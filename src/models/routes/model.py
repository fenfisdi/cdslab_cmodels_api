from pydantic import BaseModel, Field


class NewModel(BaseModel):
    name: str = Field(..., max_length=50)
    state_variables: list = Field(...)
    parameters: list = Field(...)
