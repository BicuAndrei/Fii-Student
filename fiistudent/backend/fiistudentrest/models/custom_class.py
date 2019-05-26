from fiistudentrest.models.base import BaseModel, ndb

from .schedule_class import ScheduleClass
from .student import Student

class CustomClass(BaseModel):

    """ A custom class item """

    student = ndb.KeyProperty(kind=Student)
    scheduleClass = ndb.KeyProperty(kind=ScheduleClass)
