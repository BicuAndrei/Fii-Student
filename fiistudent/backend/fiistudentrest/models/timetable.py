import ndb_orm as ndb

from . import ScheduleClass

class Timetable(BaseModel):
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
