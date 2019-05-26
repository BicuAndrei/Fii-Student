from fiistudentrest.models.base import BaseModel, ndb

from .student import Student
from .professor import Professor
from .course import Course


class Feedback(BaseModel):
    """ Feedback from a student to a professor for a certain class"""

    student = ndb.KeyProperty(kind=Student, required=True)
    professor = ndb.StringProperty(required=True)
    course = ndb.StringProperty(required=True)
    text = ndb.StringProperty()
    stars = ndb.IntegerProperty()
