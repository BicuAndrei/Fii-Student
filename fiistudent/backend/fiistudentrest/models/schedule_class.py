from fiistudentrest.models.base import BaseModel, ndb

from . import Classroom
from . import Course

class ScheduleClass(BaseModel):

    """Details about the subjects held in that classroom."""

    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.IntegerProperty()
    endHour = ndb.IntegerProperty()
    group = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom)
    course = ndb.KeyProperty(kind=Course)

