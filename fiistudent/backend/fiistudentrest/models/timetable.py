from fiistudentrest.models.base import BaseModel, ndb

from . import ScheduleClass

class Timetable(BaseModel):
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
