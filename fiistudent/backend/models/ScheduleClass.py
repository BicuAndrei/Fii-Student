import ndb_orm as ndb

class ScheduleClass(ndb.Model):
    id = ndb.StringProperty()
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    id_classroom = ndb.StringProperty()
    id_professor = ndb.StringProperty()
