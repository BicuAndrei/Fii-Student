import ndb_orm as ndb

class Timetable(ndb.Model):
    id = ndb.StringProperty()
    id_scheduleclass = ndb.StringProperty()
