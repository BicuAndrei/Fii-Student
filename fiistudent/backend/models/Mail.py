import ndb_orm as ndb

class Mail(ndb.Model):
    cc = ndb.StringProperty()
    bcc = ndb.StringProperty()
    subject = ndb.StringProperty()