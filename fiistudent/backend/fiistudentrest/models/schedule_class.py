from fiistudentrest.models.base import BaseModel, ndb

from .classroom import Classroom
from .course import Course
from .professor import Professor

class ScheduleClass(BaseModel):

    """Details about the subjects held in that classroom."""

    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.IntegerProperty()
    endHour = ndb.IntegerProperty()
    group = ndb.StringProperty()
    classType = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom)
    course = ndb.KeyProperty(kind=Course)
    professors = ndb.KeyProperty(kind=Professor)

