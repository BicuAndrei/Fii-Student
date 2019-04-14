from fiistudentrest.models.base import BaseModel, ndb

class Course(BaseModel):
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    semester= ndb.IntegerProperty()
    credits = ndb.IntegerProperty()
    link = ndb.StringProperty()
