import ssl
from urllib.request import urlopen

from bs4 import BeautifulSoup
from fiistudentrest.models import Professor


class ProfessorCrawler:
    def __init__(self, firstName, lastName, type, email, office, link):
        self.firstName = firstName
        self.lastName = lastName
        self.type = type
        self.email = email
        self.office = office
        self.link = link

    def __str__(self):
        return "%s %s\nType: %s\nEmail: %s\nOffice: %s\nLink: %s\n" % (
            self.firstName, self.lastName, self.type, self.email, self.office, self.link)

    def __eq__(self, other):
        return self.firstName == other.firstName and self.lastName == other.lastName and self.type == other.title and self.email == other.email and self.office == other.office and self.link == other.link


def get_professors():
    professors = []
    context = ssl._create_unverified_context()
    url = 'https://www.info.uaic.ro/personal-academic/'
    page = urlopen(url, context=context)  # for the HTTPS warning
    soup = BeautifulSoup(page, 'html.parser')
    professor_blocks = soup.findAll('div', class_="post-excerpt")
    for block in professor_blocks:
        # get full name first
        fullName = str(block.text)
        if fullName[0:4] == 'Dr. ':
            fullName = fullName[4:]
        fullName = fullName.partition(',')[0]

        # particular case, "Birou: Corp C" was concatenated with name
        if "Birou: Corp C" in fullName:
            fullName = fullName.replace('Birou: Corp C', '')

        # get first name
        firstName = fullName
        firstName = firstName[:firstName.rfind(' ')]

        # get last name
        lastName = fullName
        lastName = lastName[lastName.rfind(' ') + 1:]

        # get type
        type = str(block.text)
        if "universitar" in type:
            type = type[type.find(',') + 2:type.find(' universitar')]
        else:
            type = ""

        # get office
        office = str(block.text)
        if "Birou:" in office:
            office = office[office.find('Birou:') + 7:office.find('Adresa')]
        else:
            office = ""

        # get link
        link = str(block.text)
        if "Adresa Web:" in link:
            link = link[link.find('Adresa Web:') + 12:link.find('Email')]
        else:
            link = ""

        # get email
        email = str(block.text)
        if "Email:" in email:
            email = email[email.find('Email: ') + 7:email.rfind('.ro') + 3]
        else:
            email = ""

        professor = ProfessorCrawler(firstName, lastName, type, email, office, link)
        professors.append(professor)

    return professors


def ent_exists(entity):
    query = entity.query()
    query.add_filter('firstName', '=', entity.firstName)
    query.add_filter('lastName', '=', entity.firstName)
    queries = query.fetch()
    for my_query in queries:
        if my_query.first_name != "" and entity.firstName == my_query.first_name:
            if my_query.last_name != "" and entity.lastName == my_query.last_name:
                return True
    return False


def populate_datastore():
    profs = get_professors()
    for prof in profs:
        professor = Professor(
            firstName=prof.firstName,
            lastName=prof.lastName,
            type=prof.type,
            email=prof.email,
            office=prof.office,
            link=prof.link
        )
        professor.put()


def add_missing_profs():
    missing_profs = ["Simion Emil",
                     "Gavrilut Dragos",
                     "Vitcu Anca",
                     "Curelaru Versavia",
                     "Iacob Florin",
                     "Cusmuliuc Ciprian",
                     "Coman Alexandru"]

    for prof in missing_profs:
        new_prof = Professor()
        names = prof.split(" ")
        new_prof.lastName = names[0]
        new_prof.firstName = names[1]
        new_prof.put()

def clear_entries():
    all_profs = Professor.all()
    for prof in all_profs:
        prof.remove()


def main():
    clear_entries()
    populate_datastore()
    add_missing_profs()


if __name__ == '__main__':
    main()
