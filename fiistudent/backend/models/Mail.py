import ndb_orm as ndb

class Mail(ndb.Model):
    id = ndb.StringProperty()
    cc = ndb.StringProperty()
    bcc = ndb.StringProperty()
    subject = ndb.StringProperty()