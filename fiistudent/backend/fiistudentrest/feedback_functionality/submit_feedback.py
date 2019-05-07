import hug
import json

from fiistudentrest.models import Student
from fiistudentrest.models.feedback import Feedback
from fiistudentrest.auth import verify_token


@hug.local()
@hug.get()
@hug.cli()
def submit_feedback(request, professor: hug.types.number, date: hug.types.text, stars: hug.types.number,
                    feedback: hug.types.text):
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
    entity_feedback = feedback_exists(professor, student, date)
    if entity_feedback is not None:
        data["feedbackSubmitted"] = True
        data["stars"] = entity_feedback.stars
        data["feedback"] = entity_feedback.text
    else:
        data["feedbackSubmitted"] = False
        data["profId"] = professor
        data["stars"] = stars
        data["feedback"] = feedback
        # add feedback to db
        feedback_db = Feedback(
            student=student,
            professor=professor,
            # course=feedback.course, ?????
            text=feedback,
            stars=stars,
        )
        feedback_db.put()

    data_list.append(data)
    json_data = json.dumps(data_list)
    return json_data


def feedback_exists(professor, student, date):
    # checks if feedback exists from a user to a professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query.add_filter('student', '=', student)
    query.add_filter('created_at', '=', date)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            print('The professor has not received any feedback from this user at this date.')
        else:
            print('The user has submitted feedback for this professor at this date.')
            return ent
    return None


def get_all_feedback():
    # gets all feedback
    feedback_query = Feedback.query()
    feedback_query_it = feedback_query.fetch()
    data_list = []
    for ent in feedback_query:
        data = {}
        data['stars'] = ent.stars
        data['feedback'] = ent.text
        data['date'] = ent.created_at


def get_feedback_by_professor(professor):
    # filter feedback by professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query_it = query.fetch()
    return query_it


def get_feedback_by_professor_date(professor, start_date, end_date):
    # filter feedback by date and professor
    query = Feedback.query()
    query.add_filter('professor', '=', professor)
    query.add_filter('created_at', '>=', start_date)
    query.add_filter('created_at', '<=', end_date)
    query_it = query.fetch()
    return query_it


if __name__ == '__main__':
    submit_feedback.interface.cli()
