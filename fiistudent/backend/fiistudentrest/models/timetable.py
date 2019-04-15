import ndb_orm as ndb

from . import ScheduleClass

class Timetable(ndb.Model):

    """The list of all courses."""

    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
