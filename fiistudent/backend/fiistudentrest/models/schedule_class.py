from fiistudentrest.models.base import BaseModel, ndb

from . import Classroom
from . import Course

class ScheduleClass(BaseModel):
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom, required=True)
    course = ndb.KeyProperty(kind=Course, required=True)

