from fiistudentrest.models import Classroom, ScheduleClass
import ndb_orm as ndb

classroom = Classroom()
query = classroom.query()
querys = query.fetch()
for result in querys:
    schedule = ScheduleClass(classroom=result.key)
