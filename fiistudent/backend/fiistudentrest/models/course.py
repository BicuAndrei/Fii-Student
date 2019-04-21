from fiistudentrest.models.base import BaseModel, ndb

class Course(BaseModel):

    """Details about the course."""
    
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    semester= ndb.IntegerProperty()
    credits = ndb.IntegerProperty()
    link = ndb.StringProperty()
    sub_desc = ndb.StringProperty()
    studies = ndb.StringProperty()
    optional = ndb.BooleanProperty()
