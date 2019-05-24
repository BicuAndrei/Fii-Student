from fiistudentrest.models.base import BaseModel, ndb

from .student import Student
from .professor import Professor

class Token(BaseModel):

    """The token of a logged in user."""

    token = ndb.StringProperty()
    user = ndb.KeyProperty(kind=Student, required=True)
    user = ndb.KeyProperty(kind=Professor, required=True)
