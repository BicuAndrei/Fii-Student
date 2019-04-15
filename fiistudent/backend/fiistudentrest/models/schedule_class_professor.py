from fiistudentrest.models.base import BaseModel, ndb

from . import Professor
from . import ScheduleClass

class ScheduleClassProfessor(BaseModel):

    """Make the connection between professor and schedule_class."""
    
    professor = ndb.KeyProperty(kind=Professor, required=True)
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)

