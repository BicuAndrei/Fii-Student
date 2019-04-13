import hashlib
import json
from shutil import rmtree
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning   #disable la warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bs4 import BeautifulSoup


link_licenta = "https://www.info.uaic.ro/programs/informatica-ro-en/"
link_masters = "https://www.info.uaic.ro/studii-de-master/"

master_inside_links=[]


license_classes = {}

master_classes = {}

def parse_license_line(line):
    """
    Parseaza o linie din script-ul de pe https://www.info.uaic.ro/programs/informatica-ro-en/
    :param line: linia
    """
    global license_classes
    pieces = line.split("|")
    year = "An"+pieces[0]
    sem = "Sem"+pieces[1]
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
    new_class['name'] = name
    new_class['page'] = course_page
    new_class['optional'] = optional
    new_class['mandatory'] = fac
    new_class['course_index'] = pieces[2]
    license_classes[year][sem].append(new_class)


def mark_optional_license_courses():
    """
    Marcheaza materiile optionale ca fiind optionale in dictionar
    """
    global license_classes
    for year in license_classes:
        for sem in license_classes[year]:
            for i,my_class in enumerate(license_classes[year][sem]):
                if my_class["optional"] == True:
                    continue
                for j,other_class in enumerate(license_classes[year][sem]):
                    if my_class["name"] != other_class["name"] and my_class["course_index"] == other_class["course_index"]:
                        license_classes[year][sem][i]["optional"] = True
                        license_classes[year][sem][j]["optional"] = True
                        break

def parse_license_classes_page():
    """
    Intra pe https://www.info.uaic.ro/programs/informatica-ro-en/ si parseaza linie cu linie materiile
    """
    mystr = requests.get(link_licenta,verify=False) #nu merge fara verify = false
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
            for i,my_class in enumerate(master_classes[master][year][sem]):
                if my_class["optional"] == True:
                    continue
                for j,other_class in enumerate(master_classes[master][year][sem]):
                    if my_class["name"] != other_class["name"] and my_class["course_index"] == other_class["course_index"]:
                        master_classes[master][year][sem][i]["optional"] = True
                        master_classes[master][year][sem][j]["optional"] = True
                        break


def parse_master_line(line,master):
    global master_classes
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
    if year not in master_classes[master]:
        master_classes[master][year] = {}
    if sem not in master_classes[master][year]:
        master_classes[master][year][sem] = []
    new_class = {}
    new_class['name'] = name
    new_class['page'] = course_page
    new_class['optional'] = optional
    new_class['mandatory'] = fac
    new_class['course_index'] = pieces[2]
    master_classes[master][year][sem].append(new_class)



def crawl_masters_page(page,master):
    mystr = requests.get(page, verify=False)  # nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    scripts = soup.find_all("script")
    buffer = scripts[1].text.split("rawData = `")[1]
    for line in buffer.split("\n"):
        parse_master_line(line,master)


def main():
    parse_license_classes_page()
    get_masters_links()
    master_names = list(master_classes.keys())
    for i,link in enumerate(master_inside_links):
        crawl_masters_page(link,master_names[i])
        mark_optional_master_courses(master_names[i])






if __name__ == "__main__":
    main()