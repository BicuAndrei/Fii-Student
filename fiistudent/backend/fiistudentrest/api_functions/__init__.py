from .announcement import add_new_announcement
from .auth import confirm_email, login, verify_token
from .auth import confirm_forgot_password_token, register
from .auth import register as register_professor
from .change_details import change_password, change_group
from .courses import courses
from .feedback import submit_feedback, get_feedback_by_professor
from .free_rooms import free_rooms
from .professors import professors
from .quick_mail import quickmail
from .schedule import schedule
from .preferences import add_preference
