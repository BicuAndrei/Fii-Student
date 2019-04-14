import ndb_orm as ndb

class Announcement(BaseModel):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()