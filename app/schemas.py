from pydantic import BaseModel, field_validator


class CreateUser(BaseModel):
    firstname: str
    fathername: str
    lastname: str
    username: str
    email: str
    password: str

    @field_validator('firstname', 'lastname')
    @classmethod
    def names_check(cls, name):
        if name.isalpha():
            return name.capitalize()
        raise ValueError('Only letters in names, please')
