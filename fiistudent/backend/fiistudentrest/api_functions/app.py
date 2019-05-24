from .announcement import add_new_announcement
from .auth import login
from .auth import register
from .auth import confirm_forgot_password_token
from .auth import register_professor
from .courses import courses
from .change_details import change_group, change_password
from .feedback import submit_feedback, get_feedback_by_professor
from .free_rooms import free_rooms
from .professors import professors
from .quick_mail import quickmail
from .schedule import schedule

import hug

app = hug.API(__name__)
app.http.add_middleware(hug.middleware.CORSMiddleware(app))

hug.put('/announcement',api=app)(add_new_announcement)
hug.post('/change_group',api=app)(change_group)
hug.post('/change_password',api=app)(change_password)
hug.get('/courses',api=app)(courses)
hug.get('/feedback',api=app)(get_feedback_by_professor)
hug.post('/feedback', api=app)(submit_feedback)
hug.post('/forgot_password',api=app)(confirm_forgot_password_token)
hug.get('/free_rooms',api=app)(free_rooms)
hug.get('/login', api=app)(login)
hug.get('/professors',api=app)(professors)
hug.get('/quickmail',api=app)(quickmail)
hug.put('/register', api=app)(register)
hug.put('/register_professor', api=app)(register_professor)
hug.get('/schedule',api=app)(schedule)
