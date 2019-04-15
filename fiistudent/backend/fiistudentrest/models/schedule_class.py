import ndb_orm as ndb

from . import Classroom
from . import Professor

class ScheduleClass(ndb.Model):

    """Details about the subjects held in that classroom."""

    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom, required=True)
    professor = ndb.KeyProperty(kind=Professor, required=True)

