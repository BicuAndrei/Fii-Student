from fiistudentrest.models import Student, Professor, Course, Feedback
from fiistudentrest.api_functions.auth import verify_token

import hug
import json
from datetime import datetime


@hug.local()
@hug.post()
@hug.cli()
def submit_feedback(request, professor: hug.types.text, course: hug.types.text, date: hug.types.text,
                    stars: hug.types.number, feedback: hug.types.text):
    """Adds new feedback for the given professor and course"""
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
        data["alreadySubmitted"] = True
        data["course"] = Course.get(course).urlsafe
        data["stars"] = entity_feedback.stars
        data["feedback"] = entity_feedback.text
    else:
        data["alreadySubmitted"] = False
        data["profId"] = Professor.get(professor).urlsafe
        data["course"] = Course.get(course).urlsafe
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
    if query_it is not None:
        for ent in query_it:
            print(ent)
            existing_feedback_week = get_week(ent.created_at)
            if existing_feedback_week == feedback_week:
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
    return datetime.date(date).strftime("%V")


if __name__ == '__main__':
    submit_feedback.interface.cli()
