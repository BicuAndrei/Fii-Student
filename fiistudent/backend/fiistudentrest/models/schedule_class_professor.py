import ndb_orm as ndb

from . import Professor
from . import ScheduleClass


class ScheduleClassProfessor(ndb.Model):

    """Make the connection between professor and schedule_class."""

    professor = ndb.KeyProperty(kind=Professor, required=True)
    scheduleclass = ndb.KeyProperty(kind=ScheduleClass, required=True)

