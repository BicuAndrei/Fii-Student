from fiistudentrest.models.base import BaseModel, ndb

from . import Student

class Token(BaseModel):

    """The token of a logged in user."""

    token = ndb.StringProperty()
    user = ndb.KeyProperty(kind=Student,required=True)
