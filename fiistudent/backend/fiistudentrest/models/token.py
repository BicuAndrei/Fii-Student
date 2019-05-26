from fiistudentrest.models.base import BaseModel, ndb

from .student import Student
from .professor import Professor

class Token(BaseModel):

    """The token of a logged in user."""

    token = ndb.StringProperty()
    user_student = ndb.KeyProperty(kind=Student)
    user_professor = ndb.KeyProperty(kind=Professor)
