import hug
from fiistudentrest.announcement import add_new_announcement
from fiistudentrest.auth import login
from fiistudentrest.auth import register, confirm_email
from fiistudentrest.auth import confirm_forgot_password_token
from fiistudentrest.auth import register_professor
from fiistudentrest.courses_page import courses
from fiistudentrest.quick_mail import quickmail
from fiistudentrest.schedule import schedule
from fiistudentrest.api import free_rooms
from fiistudentrest.professors_page import professors
from fiistudentrest.feedback_functionality import submit_feedback
from fiistudentrest.feedback_by_professor import get_feedback_by_professor
app = hug.API(__name__)
app.http.add_middleware(hug.middleware.CORSMiddleware(app))
hug.get('/login', api=app)(login)
hug.put('/register', api=app)(register)
hug.get('/confirm_email', api=app)(confirm_email)
hug.post('/forgot_password',api=app)(confirm_forgot_password_token)
hug.put('/register_proffesor', api=app)(register_professor)
hug.get('/courses',api=app)(courses)
hug.get('/quickmail',api=app)(quickmail)
hug.get('/schedule',api=app)(schedule)
hug.get('/free_rooms',api=app)(free_rooms)
hug.get('/professors',api=app)(professors)
hug.post('/feedback', api=app)(submit_feedback)
hug.get('/feedback',api=app)(get_feedback_by_professor)
hug.put('/announcement',api=app)(add_new_announcement)
