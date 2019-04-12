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


materii_licenta = {}

def parse_license_line(line):
    global materii_licenta
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
    if year not in materii_licenta:
        materii_licenta[year] = {}
    if sem not in materii_licenta[year]:
        materii_licenta[year][sem] = []
    new_class = {}
    new_class['name'] = name
    new_class['page'] = course_page
    new_class['optional'] = optional
    new_class['mandatory'] = fac
    new_class['course_index'] = pieces[2]
    materii_licenta[year][sem].append(new_class)


def mark_optional_license_courses():
    global materii_licenta
    for year in materii_licenta:
        for sem in materii_licenta[year]:
            for i,my_class in enumerate(materii_licenta[year][sem]):
                if my_class["optional"] == True:
                    continue
                for j,other_class in enumerate(materii_licenta[year][sem]):
                    if my_class["name"] != other_class["name"] and my_class["course_index"] == other_class["course_index"]:
                        materii_licenta[year][sem][i]["optional"] = True
                        materii_licenta[year][sem][j]["optional"] = True
                        break

def parse_licenta():
    mystr = requests.get(link_licenta,verify=False) #nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    script = soup.find_all("script")[1]
    all_code = script.text.split("rawData = `")[1]
    for line in all_code.split("\n"):
        parse_license_line(line)
    mark_optional_license_courses()


def get_masters_links():
    mystr = requests.get(link_masters, verify=False)  # nu merge fara verify = false
    mystr = mystr.content
    soup = BeautifulSoup(mystr, 'lxml')
    a_list = soup.find_all("a")
    base = "https://www.info.uaic.ro"
    global master_inside_links
    for a in a_list:
        href = a.get("href")
        if href is None:
            continue
        if href.startswith("/") and base not in href:
            master_inside_links.append(base + href)



def main():
    parse_licenta()
    get_masters_links()
    for link in master_inside_links:
        print(link)




if __name__ == "__main__":
    main()