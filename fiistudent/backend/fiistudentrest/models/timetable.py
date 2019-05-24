from fiistudentrest.models.base import BaseModel, ndb

from .schedule_class import ScheduleClass

class Timetable(BaseModel):
    
    """The list of all courses."""

    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)
