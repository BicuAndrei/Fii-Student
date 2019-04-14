import hashlib
import json
import os
from shutil import rmtree

import requests
from bs4 import BeautifulSoup

folderName = "orar_FII"

crwl_pages = []

groups_schedule = {}
exams = {}
examsList = []
others = {}
othersList = []


def md5(n):
    """
    Calculeaza un hash MD5 pe un string
    :param n:
    :return:
    """
    h = hashlib.md5()
    h.update(str(n).encode('utf-8'))
    return h.hexdigest()


def update_class_dictionary(day, classes, groups, subject, type, professors, place, freq, package):
    """
    Actualizeaza orarul grupelor
    :param day:
    :param classes:
    :param groups:
    :param subject:
    :param type:
    :param professors:
    :param place:
    :param freq:
    :param package:
    """
    global groups_schedule
    general_groups = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    newClass = {}
    newClass['ora'] = classes
    newClass['materie'] = subject
    newClass['tip'] = type
    newClass['profesori'] = professors
    newClass['sala'] = place
    newClass['frecventa'] = freq
    newClass['pachet'] = package
    my_md5 = md5(newClass)
    newClass['MD5'] = my_md5

    for grupa in groups:
        if grupa in general_groups:
            for myGrupa in groups_schedule:
                if myGrupa.startswith(grupa):
                    if day not in groups_schedule[myGrupa]:
                        groups_schedule[myGrupa][day] = []
                    already = False
                    for classes in groups_schedule[myGrupa][day]:
                        if classes['MD5'] == newClass['MD5']:
                            already = True
                            break
                    if already:
                        continue
                    groups_schedule[myGrupa][day].append(newClass)
            continue
        if grupa not in groups_schedule:
            groups_schedule[grupa] = {}
        if day not in groups_schedule[grupa]:
            groups_schedule[grupa][day] = []
        already = False
        for classes in groups_schedule[grupa][day]:
            if md5(classes) == my_md5:
                already = True
        if already:
            continue
        groups_schedule[grupa][day].append(newClass)


def parse_row(row, day, update):
    """
    Proceseaza un rand din tabel
    :param row:
    :param day:
    :param update:
    :return:
    """
    tds = row.find_all("td")
    ore = tds[0].text[1:] + "-" + tds[1].text[1:]
    grupe = []
    for grupa in tds[2].find_all("a"):
        text = grupa.text.replace("\n", "").replace(" ", "").replace("\r", "")
        grupe.append(text)
    materie = tds[3].text[1:].replace("\n", "").replace("\r", "")
    tip = tds[4].text[1:].replace("\n", "").replace("\r", "")
    profesori = []
    for ref in tds[5].find_all("a"):
        profesori.append(ref.text.replace("\n", "").replace("\r", ""))
    detalii_sala = []
    for ref in tds[6].find_all("a"):
        detalii_sala.append(ref.text.replace("\n", "").replace("\r", "").replace(" ", ""))
    frecventa = tds[7].text.replace(" ", "").replace("\r", "").replace("\n", "").replace("\xa0", " ")
    pachet = tds[8].text.replace(" ", "").replace("\r", "").replace("\n", "").replace("\xa0", " ")
    if update == True:
        update_class_dictionary(day, ore, grupe, materie, tip, profesori, detalii_sala, frecventa, pachet)
        return
    return [day, ore, grupe, materie, tip, profesori, detalii_sala, frecventa, pachet]


def update_exams_dictionary(group, exam):
    """
    Actualizeaza orarul examenelor
    :param group:
    :param exam:
    :return:
    """
    global exams
    general_groups = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    if group in general_groups:
        for myGroup in exams:
            if myGroup.startswith(group):
                already = False
                for examen in exams[myGroup]:
                    if examen['MD5'] == exam['MD5']:
                        already = True
                        break
                if already:
                    continue
                exams[myGroup].append(exam)
        return
    if group not in exams:
        exams[group] = []
    already = False
    for oldExam in exams[group]:
        if oldExam['MD5'] == exam['MD5']:
            already = True
            break
    if already:
        return
    exams[group].append(exam)


def parse_row_exams(row, day):
    """
    Proceseaza un rand din tabelul cu examene
    :param row:
    :param day:
    :return:
    """
    tds = row.find_all("td")
    ore = tds[0].text[1:] + "-" + tds[1].text[1:]
    grupe = []
    for ref in tds[2].find_all("a"):
        grupe.append(ref.text.replace("\n", "").replace("\r", "").replace(" ", ""))
    materie = tds[3].text[1:].replace("\n", "").replace("\r", "")
    tip = tds[4].text[1:].replace("\n", "").replace("\r", "")
    profesori = []
    for ref in tds[5].find_all("a"):
        profesori.append(ref.text.replace("\n", "").replace("\r", ""))
    sala = []
    for ref in tds[6].find_all("a"):
        sala.append(ref.text.replace("\n","").replace("\r","").replace(" ",""))
    return [day, ore, grupe, materie, tip, profesori, sala]


def update_exams(exams):
    """
    Creeaza un dictionar nou pentru examen si actualizeaza orarul
    :param exams:
    """
    newExam = {}
    newExam['data'] = exams[0]
    newExam['ora'] = exams[1]
    newExam['materie'] = exams[3]
    newExam['profesori'] = exams[5]
    newExam['sala'] = exams[6]
    newExam['MD5'] = md5(newExam)
    for group in exams[2]:
        update_exams_dictionary(group, newExam)


def parse_page(url):
    """
    Proceseaza o pagina de orar
    :param url:
    """
    page = requests.get(url)
    page = page.content
    soup = BeautifulSoup(page, 'lxml')
    tables = soup.find_all("table")
    tabel_normal, tabel_examene = tables[0], tables[1]
    rows = tabel_normal.find_all("tr")
    last_day = ""
    for row in rows[1:]:
        if len(row.find_all("b")) == 1:
            last_day = row.text.replace("\n", "")
            continue
        parse_row(row, last_day, True)

    global examsList, othersList
    rows = tabel_examene.find_all("tr")
    for row in rows[1:]:
        if len(row.find_all("b")) == 2:
            last_day = ""
            for b in row.find_all("b"):
                last_day = last_day + b.text.replace("\n", "")
            continue
        lista = parse_row_exams(row, last_day)
        if lista[4] == "Examen":
            examsList.append(lista)
        else:
            othersList.append(lista)


def update_others_dictionary(group, other):
    """
    Actualizeaza orarul grupelor cu elemente din tabelul de examene care nu sunt examene
    :param group:
    :param other:
    :return:
    """
    global others
    general_groups = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    if group in general_groups:
        for myGroup in others:
            if myGroup.startswith(group):
                already = False
                for knownOthers in others[myGroup]:
                    if knownOthers['MD5'] == other['MD5']:
                        already = True
                        break
                if already:
                    continue
                others[myGroup].append(other)
        return
    if group not in others:
        others[group] = []
    already = False
    for oldOther in others[group]:
        if oldOther['MD5'] == other['MD5']:
            already = True
            break
    if already:
        return
    others[group].append(other)


def update_others(lista):
    """
    Actualizeaza orarul cu alte activitati
    :param lista:
    """
    newOther = {}
    newOther['data'] = lista[0]
    newOther['ora'] = lista[1]
    newOther['materie'] = lista[3]
    newOther['tip'] = lista[4]
    newOther['profesori'] = lista[5]
    newOther['sala'] = lista[6]
    newOther['MD5'] = md5(newOther)
    for grupa in lista[2]:
        update_others_dictionary(grupa, newOther)


def crawl_website_schedule():
    """
    Proceseaza fiecare pagina de orar si actualizeaza dictionarele.
    """
    for pagina in crwl_pages:
        parse_page(pagina)
        print("Parsed -- {0}".format(pagina))
    global exams, others
    for grupa in groups_schedule:
        exams[grupa] = []
        others[grupa] = []
    for examen_lista in examsList:
        update_exams(examen_lista)
    for others_list in othersList:
        update_others(others_list)


def reset_folder(name):
    """
    Reseteaza folder-ul (il sterge si face altul nou)
    :param name:
    """
    if os.path.isdir(name):
        rmtree(name)
    os.mkdir(name)


def update_folders():
    """
    Actualizeaza toate fisierele cu informatiile gasite
    """
    for grupa in groups_schedule:
        path = os.path.join(folderName, grupa)
        reset_folder(path)
        for zi in groups_schedule[grupa]:
            fileName = zi + ".json"
            path = os.path.join(folderName, grupa, fileName)
            handle = open(path, "a+")
            handle.write(json.dumps(groups_schedule[grupa][zi], indent=4, sort_keys=True))
            handle.close()
    for grupa in exams:
        folder = os.path.join(folderName, grupa)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        file = os.path.join(folder, "Examene.json")
        handle = open(file, "a+")
        handle.write(json.dumps(exams[grupa], indent=4, sort_keys=True))
        handle.close()
    for grupa in others:
        file = os.path.join(folderName, grupa, "Others.json")
        handle = open(file, "a+")
        handle.write(json.dumps(others[grupa], indent=4, sort_keys=True))
        handle.close()


def get_schedule_pages():
    """
    Intra pe https://profs.info.uaic.ro/~orar/orar_studenti.html si ia link-urile ce urmeaza sa fie crawlate
    """
    global crwl_pages
    base = "https://profs.info.uaic.ro/~orar/"
    url = "https://profs.info.uaic.ro/~orar/orar_studenti.html"
    page = requests.get(url)
    page = page.content
    soup = BeautifulSoup(page, 'lxml')
    found_groups = []
    a_items = soup.find_all("a")
    for a_item in a_items[1:-1]:
        link = a_item.get("href")
        not_ok = False
        group = link.split("_")[1].replace(".html", "")
        for fgroup in found_groups:
            if fgroup in group:
                not_ok = True
                break
        if not_ok:
            continue
        found_groups.append(group)
        crwl_pages.append(base + link)


def main():
    get_schedule_pages()
    crawl_website_schedule()
    reset_folder(folderName)
    update_folders()


if __name__ == "__main__":
    main()
