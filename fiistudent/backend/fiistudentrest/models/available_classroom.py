from fiistudentrest.models.base import BaseModel, ndb

from .classroom import Classroom


class AvailableClassroom(BaseModel):

    """Location and capacity information of a classroom."""

    dayOfTheWeek = ndb.StringProperty()
    startHour = ndb.IntegerProperty()
    endHour = ndb.IntegerProperty()
    classroom = ndb.KeyProperty(kind=Classroom)
