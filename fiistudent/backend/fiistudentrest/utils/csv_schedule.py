import csv
import datetime
import sys

from fiistudentrest.models import ScheduleClass, Course, Classroom


def get_datastore_info(group):
    sch = ScheduleClass()
    query = sch.query()
    query.add_filter('group', '=', group)
    querys = query.fetch()
    info = []
    for found in querys:
        info.append(found)
    if len(info) is 0:
        return False
    return info


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def get_course(key):
    if key is None:
        return False
    course = Course()
    course = course.get(key)
    return course.title


def get_class(key):
    if key is None:
        return False
    try:
        classroom = Classroom.get(key)
        return classroom.identifier
    except:
        return False


def get_printable_rows(datastore_rows):
    rows = []
    for row in datastore_rows:
        printable_row = {'day': row.dayOfTheWeek,
                         'start': row.startHour,
                         'end': row.endHour,
                         'tip': row.classType}
        course = get_course(row.course)
        if course is False:
            printable_row['curs'] = "-"
        else:
            printable_row['curs'] = course
        classroom = get_class(row.classroom)
        if classroom is False:
            printable_row['sala'] = "-"
        else:
            printable_row['sala'] = classroom
        rows.append(printable_row)
    return rows


def get_file(grup):
    return open(grup + "_schedule.csv", "w")


def get_ordered_day_itmes(day, rows):
    items = []
    ordered_items = []
    remove = []
    for i, row in enumerate(rows):
        if rows[i]['day'] == day:
            items.append(rows[i])
            remove.append(i)
    if len(items) == 0:
        return False
    k = 0
    for index in remove:
        del rows[index - k]
        k += 1
    while len(items) != 0:
        min = items[0]['start']
        min_index = 0
        for i in range(1, len(items)):
            if items[i]['start'] < min:
                min = items[i]['start']
                min_index = i
        ordered_items.append(items[min_index])
        del items[min_index]
    return ordered_items


def get_date(dayIndex):
    currDate = datetime.datetime.now()
    currDate = str(datetime.datetime.date(currDate))
    currDate = currDate.split("-")
    d = datetime.date(int(currDate[0]), int(currDate[1]), int(currDate[2]))
    next_day = next_weekday(d, dayIndex)
    next_day = str(next_day).split("-")
    return next_day[1] + "/" + next_day[2] + "/" + next_day[0]


def main():
    for i in range(1, len(sys.argv)):
        info = get_datastore_info(sys.argv[i])
        if info is False:
            print("[ ERROR ] No info found for [{0}]".format(sys.argv[i]))
            continue
        days = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
        rows = get_printable_rows(info)
        file = get_file(sys.argv[i])
        writer = csv.writer(file)
        writer.writerow(
            ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location',
             'Private'])
        for i, day in enumerate(days):
            classes = get_ordered_day_itmes(day, rows)
            if classes is False:
                continue
            for myclass in classes:
                writer.writerow(
                    [myclass['curs'], get_date(i), str(myclass['start']) + ":00", get_date(i),
                     str(myclass['end']) + ":00", 'False', myclass['tip'], myclass['sala'], 'True'])
        print("[ CSV ] Schedule for [{0}] has been exported.".format(sys.argv[i]))
        file.close()


if __name__ == "__main__":
    main()
