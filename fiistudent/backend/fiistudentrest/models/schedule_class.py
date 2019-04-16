from fiistudentrest.models.base import BaseModel, ndb

from . import Classroom
from . import Course

class ScheduleClass(BaseModel):

    """Details about the subjects held in that classroom."""

    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    group = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom, required=True)
    course = ndb.KeyProperty(kind=Course, required=True)

