import requests
import unidecode
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # disable la warning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
from fiistudentrest.models import Course

link_licenta = "https://www.info.uaic.ro/programs/informatica-ro-en/"
link_masters = "https://www.info.uaic.ro/studii-de-master/"

master_inside_links = []

license_classes = {}

master_classes = {}


def parse_license_line(line):
    """
    Parseaza o linie din script-ul de pe https://www.info.uaic.ro/programs/informatica-ro-en/
    :param line: linia
    """
    global license_classes
    pieces = line.split("|")
    year = "An" + pieces[0]
    sem = "Sem" + pieces[1]
    if "F" in pieces[2]:
        fac = False
    else:
        fac = True
    name = pieces[3]
    course_page = pieces[6]
    optional = False
    if year not in license_classes:
        license_classes[year] = {}
    if sem not in license_classes[year]:
        license_classes[year][sem] = []
    new_class = {}
    new_class['name'] = unidecode.unidecode(name)
    new_class['page'] = course_page
    new_class['optional'] = optional
    new_class['mandatory'] = fac
    new_class['course_index'] = pieces[2]
    new_class['credits'] = pieces[4]
    license_classes[year][sem].append(new_class)


def mark_optional_license_courses():
    """
    Marcheaza materiile optionale ca fiind optionale in dictionar
    """
    global license_classes
    for year in license_classes:
        for sem in license_classes[year]:
            for i, my_class in enumerate(license_classes[year][sem]):
                if my_class["optional"] == True:
                    continue
                for j, other_class in enumerate(license_classes[year][sem]):
                    if my_class["name"] != other_class["name"] and my_class["course_index"] == other_class[
                        "course_index"]:
                        license_classes[year][sem][i]["optional"] = True
                        license_classes[year][sem][j]["optional"] = True
                        break


def parse_license_classes_page():
    """
    Intra pe https://www.info.uaic.ro/programs/informatica-ro-en/ si parseaza linie cu linie materiile
    """
    mystr = requests.get(link_licenta, verify=False)  # nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    script = soup.find_all("script")[1]
    all_code = script.text.split("rawData = `")[1]
    for line in all_code.split("\n"):
        parse_license_line(line)
    mark_optional_license_courses()


def get_masters_links():
    """
    Ia link-urile cu materiile de la master
    """
    mystr = requests.get(link_masters, verify=False)  # nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    a_list = soup.find_all("a")
    base = "https://www.info.uaic.ro"
    global master_inside_links
    global master_classes
    for a in a_list:
        href = a.get("href")

        if href is None:
            continue
        if href.startswith("/") and base not in href:
            master_classes[a.text] = {}
            master_inside_links.append(base + href)


def mark_optional_master_courses(master):
    """
    Marcheaza materiile optionale ca fiind optionale in dictionar
    """
    global master_classes
    for year in master_classes[master]:
        for sem in master_classes[master][year]:
            for i, my_class in enumerate(master_classes[master][year][sem]):
                if my_class["optional"] == True:
                    continue
                for j, other_class in enumerate(master_classes[master][year][sem]):
                    if my_class["name"] != other_class["name"] and my_class["course_index"] == other_class[
                        "course_index"]:
                        master_classes[master][year][sem][i]["optional"] = True
                        master_classes[master][year][sem][j]["optional"] = True
                        break


def parse_master_line(line, master):
    """
    Parseaza o linie din script-ul de pe pagina materiilor de la master-ul mentionat
    :param line: linia
    :param master: Numele master-ului
    """
    global master_classes
    pieces = line.split("|")
    year = "An" + pieces[0]
    sem = "Sem" + pieces[1]
    if "F" in pieces[2]:
        fac = False
    else:
        fac = True
    name = pieces[3]
    if "Discipline opţionale:" in name:
        return
    if pieces[6] != "`;":
        course_page = pieces[6]
    else:
        course_page = " "
    optional = False
    if year not in master_classes[master]:
        master_classes[master][year] = {}
    if sem not in master_classes[master][year]:
        master_classes[master][year][sem] = []
    new_class = {}
    new_class['name'] = unidecode.unidecode(name)
    new_class['page'] = course_page
    new_class['optional'] = optional
    new_class['mandatory'] = fac
    new_class['course_index'] = pieces[2]
    new_class['credits'] = pieces[4]
    master_classes[master][year][sem].append(new_class)


def crawl_masters_page(page, master):
    """
    Intra pe pagina master-ului si ia materiile sale
    :param page: link-ul
    :param master: numele master-ului
    """
    mystr = requests.get(page, verify=False)  # nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    scripts = soup.find_all("script")
    buffer = scripts[1].text.split("rawData = `")[1]
    for line in buffer.split("\n"):
        parse_master_line(line, master)


def ent_exists(entity):
    query = entity.query()
    query.add_filter('title', '=', entity.title)
    querys = query.fetch()
    for my_query in querys:
        if my_query.title != "" and entity.studies == my_query.studies:
            return True
    return False


def update_classes(year, sem, studies, my_class):
    """
    Face update unei materii in tabel
    :param year: anul
    :param sem: semestrul
    :param studies: licenta/nume_master
    :param my_class: dictionar cu informatii despre materie
    """
    course = Course(
        title=my_class['name'],
        year=int(year.replace("An", "")),
        semester=int(sem.replace("Sem", "")),
        credits=int(my_class['credits']),
        link=my_class['page'],
        studies=studies
    )
    if not ent_exists(course):
        course.put()


def empty_entity():
    course = Course()
    classes = course.query().fetch()
    for c in classes:
        c.remove()
    print('remove done')


def populate_datastore():
    """
    Populeaza baza de date cu materiile de studiu
    """
    empty_entity()
    for year in license_classes:
        for sem in license_classes[year]:
            for my_class in license_classes[year][sem]:
                update_classes(year, sem, "Licenta", my_class)

    for master in master_classes:
        for year in master_classes[master]:
            for sem in master_classes[master][year]:
                for my_class in master_classes[master][year][sem]:
                    update_classes(year, sem, master, my_class)


def main():
    parse_license_classes_page()
    get_masters_links()
    master_names = list(master_classes.keys())
    for i, link in enumerate(master_inside_links):
        crawl_masters_page(link, master_names[i])
        mark_optional_master_courses(master_names[i])
    populate_datastore()
    course = Course(
        title='Managementul proiectelor',
        year=2,
        semester=2,
        credits=0,
        link='',
        studies=''
    )
    course.put()
    course = Course(
        title='Programare competitiva II, facultativ, pregatire olimpiada',
        year=3,
        semester=2,
        credits=0,
        link='',
        studies='Licenta'
    )
    course.put()

if __name__ == "__main__":
    main()
