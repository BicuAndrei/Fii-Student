"""Here are all NDB models."""


from .alert import Alert
from .announcement import Announcement
from .base import BaseModel, NAMESPACE, ndb
from .course import Course
from .classroom import Classroom
from .link import Link
from .mail import Mail
from .professor import Professor
from .schedule_class import ScheduleClass
from .schedule_class_professor import ScheduleClassProfessor
from .student import Student
from .timetable import Timetable
from .token import Token
from .exam import Exam
