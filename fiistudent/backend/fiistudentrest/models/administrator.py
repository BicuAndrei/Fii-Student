from backend.models.base import BaseModel, ndb

class Administrator(BaseModel):

    """Credentials and data of admins."""

    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
