from fiistudentrest.models.base import BaseModel, ndb

from . import Student, Professor

class Token(BaseModel):

    """The token of a logged in user."""

    token = ndb.StringProperty()
    user = ndb.KeyProperty(kind=Student, required=True)
    user = ndb.KeyProperty(kind=Professor, required=True)
