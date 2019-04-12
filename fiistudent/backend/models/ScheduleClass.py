import ndb_orm as ndb

import Classroom
import Professor

class ScheduleClass(ndb.Model):
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classroom = ndb.KeyProperty(kind=Classroom, required=True)
    professor = ndb.KeyProperty(kind=Professor, required=True)

