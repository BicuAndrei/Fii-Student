import ndb_orm as ndb

import Professor
import ScheduleClass


class ScheduleClassProfessor(ndb.Model):
    professor = ndb.KeyProperty(kind=Professor, required=True)
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)

