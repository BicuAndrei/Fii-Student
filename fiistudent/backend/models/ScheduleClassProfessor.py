import ndb_orm as ndb

class ScheduleClassProfessor(ndb.Model):
    id_professor = ndb.StringProperty()
    id_scheduleclass = ndb.StringProperty()