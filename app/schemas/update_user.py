from pydantic import BaseModel


class UpdateUser(BaseModel):

    full_name: str

    mobile_number: str

    is_active: bool
