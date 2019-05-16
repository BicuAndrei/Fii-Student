import hug
from fiistudentrest.auth import login
from fiistudentrest.auth import register
from fiistudentrest.courses_page import courses
from fiistudentrest.quick_mail import quickmail
from fiistudentrest.schedule import schedule
from fiistudentrest.api import free_rooms
from fiistudentrest.professors_page import professors
from fiistudentrest.feedback_functionality import submit_feedback

app = hug.API(__name__)
app.http.add_middleware(hug.middleware.CORSMiddleware(app))
hug.get('/login', api=app)(login)
hug.get('/register', api=app)(register)
hug.get('/courses',api=app)(courses)
hug.get('/quickmail',api=app)(quickmail)
hug.get('/schedule',api=app)(schedule)
hug.get('/free_rooms',api=app)(free_rooms)
hug.get('/professors',api=app)(professors)
hug.post('/feedback', api=app)(submit_feedback)
