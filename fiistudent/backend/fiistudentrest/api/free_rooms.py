from fiistudentrest.models import Classroom
from fiistudentrest.models import ScheduleClass
from fiistudentrest.auth import verify_token
import hug
import datetime
import json


def get_classes(day_of_the_week):
    """ Returneaza toate orele dintr-o anumita zi """
    query = ScheduleClass.query()
    if day_of_the_week == 0:
        query.add_filter('dayOfTheWeek', '=', 'Luni')
    elif day_of_the_week == 1:
        query.add_filter('dayOfTheWeek', '=', 'Marti')
    elif day_of_the_week == 2:
        query.add_filter('dayOfTheWeek', '=', 'Miercuri')
    elif day_of_the_week == 3:
        query.add_filter('dayOfTheWeek', '=', 'Joi')
    elif day_of_the_week == 4:
        query.add_filter('dayOfTheWeek', '=', 'Vineri')
    elif day_of_the_week == 5:
        query.add_filter('dayOfTheWeek', '=', 'Sambata')
    elif day_of_the_week == 6:
        query.add_filter('dayOfTheWeek', '=', 'Duminica')
    query_it = query.fetch()
    return list(query_it)


def get_all_classrooms():
    """ Returneaza toate salile """
    query = Classroom.all()
    return query


@hug.local()
@hug.get()
@hug.cli()
def free_rooms(request, date: hug.types.text, start_hour: hug.types.number, duration: hug.types.number):
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

    day, month, year = (int(x) for x in date.split('.'))
    date_obj = datetime.date(year, month, day)
    day_of_week = date_obj.weekday()

    # iau toate clasele si cursurile
    courses = get_classes(day_of_week)
    classrooms = get_all_classrooms()
    classrooms_dictionary = {}

    # iau fiecare curs si verific daca se afla in intervalul primit ca parametri
    for course in courses:
        aux = start_hour
        while aux < start_hour + duration:
            if course.endHour > aux >= course.startHour:
                classroom_course = course.classroom.get()
                if classroom_course in classrooms:
                    classrooms.remove(classroom_course)
                # creez un string cu intervalul orar ex: 12:00 - 14:00
                time_interval = str(course.startHour) + ':00 - ' + str(course.endHour) + ':00'
                # introduc un element pereche time_interval - lista de sali goale in acel interval
                classrooms_dictionary[time_interval] = classrooms  # classrooms e o lista
            aux = aux + 1

    data_list = []
    data = {}

    # creez raspunsul
    if len(classrooms) == 0:
        data1 = {}
        data_list1 = []

        data["status"] = "error"
        data1["for"] = "freeRooms"
        data1["message"] = "There's no free room."
        data_list1.append(data1)
        data["error"] = data_list1
        data_list.append(data)

        json_data = json.dump(data_list)

    else:
        classrooms_dictionary_items = classrooms_dictionary.items()
        # parcurg fiecare element din lista cu perechi
        for elem in classrooms_dictionary_items:
            # parcurg fiecare clasa din lista cu clase din elem[1]
            for free_classroom in elem[1]:
                data = {}
                data["room"] = free_classroom.identifier
                data["disponibility"] = elem[0]
                data_list.append(data)

        json_data = json.dumps(data_list)

    return json_data


if __name__ == '__main__':
    free_rooms.interface.cli()
