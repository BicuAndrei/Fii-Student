from fiistudentrest.models.base import BaseModel, ndb

from . import Professor
from . import ScheduleClass


class ScheduleClassProfessor(BaseModel):
    professor = ndb.KeyProperty(kind=Professor, required=True)
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)

