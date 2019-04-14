import ndb_orm as ndb

class Course(BaseModel):
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    semester= ndb.IntegerProperty()
    credits = ndb.IntegerProperty()
    link = ndb.StringProperty()
