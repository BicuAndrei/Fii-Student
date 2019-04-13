import ndb_orm as ndb

from . import ScheduleClass

class Timetable(ndb.Model):
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
