from fiistudentrest.models.base import BaseModel, ndb
from .classroom import Classroom
from .professor import Professor


class SchAnnouncement(BaseModel):

    """Information about an announcement posted on the schedule page."""

    date = ndb.StringProperty()
    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.StringProperty()
    endHour = ndb.StringProperty()
    classrooms = ndb.KeyProperty(kind=Classroom,repeated='true')
    title = ndb.StringProperty()
    professors = ndb.KeyProperty(kind=Professor,repeated='true')
    groups = ndb.StringProperty()
    type = ndb.StringProperty()
