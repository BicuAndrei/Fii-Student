import ndb_orm as ndb

import ScheduleClass

class Timetable(ndb.Model):
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
