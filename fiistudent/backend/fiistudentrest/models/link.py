from fiistudentrest.models.base import BaseModel, ndb

class Link(BaseModel):

    """The link of the discipline."""

    link = ndb.StringProperty()
    description = ndb.StringProperty()
