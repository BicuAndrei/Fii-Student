from fiistudentrest.models.base import BaseModel, ndb
from .student import Student

class Preference(BaseModel):

    """Information about students preferences."""
    
    student = ndb.KeyProperty(kind=Student)
    preference = ndb.StringProperty()
