from fiistudentrest.models import Classroom
from fiistudentrest.models import Professor
from fiistudentrest.models import Course
from fiistudentrest.models.base import BaseModel, ndb


class Exam(BaseModel):

    """Information about the exam from the schedule page."""

    date = ndb.StringProperty()
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classrooms = ndb.KeyProperty(kind=Classroom,repeated='true')
    course = ndb.KeyProperty(kind=Course)
    professors = ndb.KeyProperty(kind=Professor,repeated='true')
    groups = ndb.StringProperty()