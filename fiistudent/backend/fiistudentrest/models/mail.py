import ndb_orm as ndb

class Mail(BaseModel):
    cc = ndb.StringProperty()
    bcc = ndb.StringProperty()
    subject = ndb.StringProperty()