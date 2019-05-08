import hug
import json
import datetime
# import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Dana\\Documents\\fii-student-5c3ee6b54bbd.json"

from fiistudentrest.models import Student
from fiistudentrest.models.feedback import Feedback
from fiistudentrest.auth import verify_token


@hug.local()
@hug.get()
@hug.cli()
def submit_feedback(request, professor: hug.types.text, course: hug.types.text, date: hug.types.text,
                    stars: hug.types.number, feedback: hug.types.text):
    """
    professor = "5105779283591168"
    course = "6476246011609088"
    date = "2019-05-03 (14:52:39.712) EEST"
    stars = 5
    feedback = "Mi-a placut"
    student = Student.get("ag1lfmZpaS1zdHVkZW50chQLEgdTdHVkZW50GICAgNjGgocJDKIBC2RldmVsb3BtZW50")
    """
    authorization = request.get_header('Authorization')
    if not authorization:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'No Authorization field exists in request header'}]}

    user_urlsafe = verify_token(authorization)
    if not user_urlsafe:
        return {'status': 'error',
                'errors': [
                    {'for': 'request_header', 'message': 'Header contains token, but it is not a valid one.'}]}

    student = Student.get(user_urlsafe)
    data_list = []
    data = {}
    # check if feedback already exists
    entity_feedback = feedback_exists(professor, student, date, course)
    if entity_feedback is not None:
        data["feedbackSubmitted"] = True
        data["course"] = entity_feedback.course
        data["stars"] = entity_feedback.stars
        data["feedback"] = entity_feedback.text
    else:
        data["feedbackSubmitted"] = False
        data["profId"] = professor
        data["course"] = course
        data["stars"] = stars
        data["feedback"] = feedback
        # add feedback to db
        feedback_db = Feedback(
            student=student,
            professor=professor,
            course=course,
            text=feedback,
            stars=stars,
        )
        feedback_db.put()

    data_list.append(data)
    json_data = json.dumps(data_list)
    return json_data


def feedback_exists(professor, student, date, course):
    # checks if feedback exists from a user to a professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query.add_filter('student', '=', student)
    query.add_filter('course', '=', course)
    feedback_week = get_week(date)
    query_it = query.fetch()
    for ent in query_it:
        existing_feedback_week = get_week(ent.created_at)
        if ent is None:
            print('The professor has not received any feedback from this user at this date.')
        elif existing_feedback_week == feedback_week:
            print('The user has submitted feedback for this professor at this date.')
            return ent
    return None


def get_all_feedback():
    # gets all feedback
    feedback_query = Feedback.query()
    feedback_query_it = feedback_query.fetch()
    data_list = []
    for ent in feedback_query_it:
        data = {'stars': ent.stars, 'feedback': ent.text, 'date': ent.created_at, 'course': ent.course}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data


def get_feedback_by_professor(professor):
    # filter feedback by professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query_it = query.fetch()
    data_list = []
    for ent in query_it:
        data = {'stars': ent.stars, 'feedback': ent.text, 'date': ent.created_at, 'course': ent.course}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data


def get_feedback_by_professor_date(professor, start_date, end_date):
    # filter feedback by date and professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query.add_filter('created_at', '>=', start_date)
    query.add_filter('created_at', '<=', end_date)
    query_it = query.fetch()
    data_list = []
    for ent in query_it:
        data = {'stars': ent.stars, 'feedback': ent.text, 'date': ent.created_at, 'course': ent.course}
        data_list.append(data)

    json_data = json.dumps(data_list)
    return json_data


def get_week(date):
    # returns the number of the week for a given date
    # standard RFC 3339 for datastore is: '%Y-%m-%dT%H:%M:%S.%fZ'
    feedback_date = datetime.datetime.strptime(date,
                                               '%Y-%m-%d (%H:%M:%S.%f) EEST')
    return datetime.date(feedback_date.year, feedback_date.month, feedback_date.day).isocalendar()[1]


if __name__ == '__main__':
    submit_feedback.interface.cli()
