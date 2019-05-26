from fiistudentrest.models.base import BaseModel, ndb

from .student import Student
from .professor import Professor
from .course import Course


class Feedback(BaseModel):
    """ Feedback from a student to a professor for a certain class"""

    student = ndb.KeyProperty(kind=Student, required=True)
    professor = ndb.KeyProperty(kind=Professor, required=True)
    course = ndb.KeyProperty(kind=Course, required=True)
    text = ndb.StringProperty()
    stars = ndb.IntegerProperty()
