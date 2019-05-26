from fiistudentrest.models.base import BaseModel, ndb

from .classroom import Classroom
from .professor import Professor
from .course import Course


class Exam(BaseModel):

    """Information about the exam from the schedule page."""

    date = ndb.StringProperty()
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classrooms = ndb.KeyProperty(kind=Classroom,repeated=True)
    course = ndb.KeyProperty(kind=Course)
    professors = ndb.KeyProperty(kind=Professor,repeated=True)
    groups = ndb.StringProperty()
