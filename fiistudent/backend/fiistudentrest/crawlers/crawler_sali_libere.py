# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from fiistudentrest.models import Classroom
from fiistudentrest.models.available_classroom import AvailableClassroom


class Course:
    def __init__(self, dayy, hour1, hour2):
        self.day = dayy
        self.starthour = hour1
        self.endhour = hour2

    def __str__(self):
        return "%s %s to %s" % (self.day, self.starthour, self.endhour)

    def __eq__(self, other):
        return self.day == other.day and self.starthour == other.starthour and self.endhour == other.endhour

#contains all the pages with the labs
crawlable_pages = []
#contains all the free periods from all labs
free_days = []

def crawl_page(url):
    weekDays = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    hours = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00']
    timetableContent = []
    freePeriods = []
    timetable = []
    startHour = ''
    endHour = ''
    currentDay = ''
    global free_days
    # query the website and return the html to the variable ‘page’
    try:
        page = urlopen(url)
    except:
        return

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    for td in soup.find_all("td"):
        for day in weekDays:
            if day in td.text.strip():
                timetableContent.append(day)
        for hour in hours:
            if hour in td.text.strip():
                timetableContent.append(hour)

    for i in range(0, 5):
        day = weekDays[i]
        for j in range(0, 6):
            freePeriods.append(Course(day, hours[j], hours[j + 1]))

    for record in timetableContent:
        if record in weekDays:
            currentDay = record
        if record in hours:
            if startHour != '':
                endHour = record
            else:
                startHour = record
        if startHour != '' and endHour != '':
            timetable.append(Course(currentDay, startHour, endHour))
            if Course(currentDay, startHour, endHour) in freePeriods:
                freePeriods.remove(Course(currentDay, startHour, endHour))
            startHour = ''
            endHour = ''

    lab_name = url.split('_')[1].split('.')[0]
    free_period_lab = {'name' : lab_name, 'free_period' : freePeriods}
    free_days.append(free_period_lab)

def crawl_pages():
    global crawlable_pages
    for page in crawlable_pages:
        crawl_page(page)
        print('Crawled %s' % page)


def get_schedule_pages():
    """
            Intra pe https://profs.info.uaic.ro/~orar/orar_resure.html si ia link-urile ce urmeaza sa fie crawlate
    """

    global crawlable_pages
    base = "https://profs.info.uaic.ro/~orar/"
    url = "https://profs.info.uaic.ro/~orar/orar_resurse.html"
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    rooms = []
    a_items = soup.find_all("a")
    for a_item in range(0,len(a_items)-2):
        link = a_items[a_item].get("href")
        is_in_array_already = False
        group = link.split("_")[1].replace(".html", "")
        for room in rooms:
            if room in group:
                is_in_array_already = True
                break
        if is_in_array_already:
            continue
        rooms.append(group)
        new_page = base+link
        crawlable_pages.append(new_page)


def clear_entities():
    avb = AvailableClassroom(
        endHour=1,
        startHour=2
    )
    avbs = avb.query().fetch()
    for a in avbs:
        a.remove()


def populate_entity(period):
    avb = AvailableClassroom()
    for free_period in period['free_period']:
        avb.startHour = int(free_period.starthour.split(':')[0])
        avb.endHour = int(free_period.endhour.split(':')[0])
        avb.dayOfTheWeek = free_period.day
        print(avb)
        # trebuie sa ii mai pun cheia straina catre classroom

    #avb.put()


def populate_datastore():
    global free_days
    clear_entities()
    for period in free_days:
        populate_entity(period)

def main():
    get_schedule_pages()
    crawl_pages()
    populate_datastore()


if __name__ == "__main__":
    main()
