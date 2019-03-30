import hashlib
import json
import os
from shutil import rmtree
import requests
from bs4 import BeautifulSoup

folderName = "orar_FII"

pagini_orar = ["https://profs.info.uaic.ro/~orar/participanti/orar_I1.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_I2.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_I3.html",
               # "https://profs.info.uaic.ro/~orar/participanti/orar_I1x.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_MIS.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_MLC.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_MOC.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_MSD.html",
               "https://profs.info.uaic.ro/~orar/participanti/orar_MSI.html", ]

orar_grupe = {}
exams = {}
examsList = []
others = {}
othersList = []


def md5(n):
    h = hashlib.md5()
    h.update(str(n).encode('utf-8'))
    return h.hexdigest()


def updateDictionarOre(day, ore, grupe, materie, tip, profesori, sala, frecventa, pachet):
    global orar_grupe
    grupe_generale = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    newOra = {}
    newOra['ora'] = ore
    newOra['materie'] = materie
    newOra['tip'] = tip
    newOra['profesori'] = profesori
    newOra['sala'] = sala
    newOra['frecventa'] = frecventa
    newOra['pachet'] = pachet
    my_md5 = md5(newOra)
    newOra['MD5'] = my_md5

    for grupa in grupe:
        if grupa in grupe_generale:
            for myGrupa in orar_grupe:
                if myGrupa.startswith(grupa):
                    if day not in orar_grupe[myGrupa]:
                        orar_grupe[myGrupa][day] = []
                    deja = False
                    for ore in orar_grupe[myGrupa][day]:
                        if ore['MD5'] == newOra['MD5']:
                            deja = True
                            break
                    if deja:
                        continue
                    orar_grupe[myGrupa][day].append(newOra)
            continue
        if grupa not in orar_grupe:
            orar_grupe[grupa] = {}
        if day not in orar_grupe[grupa]:
            orar_grupe[grupa][day] = []
        deja = False
        for ore in orar_grupe[grupa][day]:
            if md5(ore) == my_md5:
                deja = True
        if deja:
            continue
        orar_grupe[grupa][day].append(newOra)


def parseRow(row, day, update):
    tds = row.find_all("td")
    ore = tds[0].text[1:] + "-" + tds[1].text[1:]
    grupe = []
    for grupa in tds[2].find_all("a"):
        text = grupa.text.replace("\n", "").replace(" ", "").replace("\r", "")
        grupe.append(text)
    materie = tds[3].text[1:]
    tip = tds[4].text[1:]
    profesori = []
    for ref in tds[5].find_all("a"):
        profesori.append(ref.text)
    detalii_sala = []
    for ref in tds[6].find_all("a"):
        detalii_sala.append(ref.text)
    frecventa = tds[7].text.replace(" ", "").replace("\r", "").replace("\n", "").replace("\xa0", " ")
    pachet = tds[8].text.replace(" ", "").replace("\r", "").replace("\n", "").replace("\xa0", " ")
    if update == True:
        updateDictionarOre(day, ore, grupe, materie, tip, profesori, detalii_sala, frecventa, pachet)
        return
    return [day, ore, grupe, materie, tip, profesori, detalii_sala, frecventa, pachet]


def updateDictionarExams(grupa, exam):
    global exams
    grupe_generale = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    if grupa in grupe_generale:
        for myGrupa in exams:
            if myGrupa.startswith(grupa):
                deja = False
                for examen in exams[myGrupa]:
                    if examen['MD5'] == exam['MD5']:
                        deja = True
                        break
                if deja:
                    continue
                exams[myGrupa].append(exam)
        return
    if grupa not in exams:
        exams[grupa] = []
    deja = False
    for oldExam in exams[grupa]:
        if oldExam['MD5'] == exam['MD5']:
            deja = True
            break
    if deja:
        return
    exams[grupa].append(exam)


def parseRowExams(row, day):
    tds = row.find_all("td")
    ore = tds[0].text[1:] + "-" + tds[1].text[1:]
    grupe = []
    for ref in tds[2].find_all("a"):
        grupe.append(ref.text.replace("\n", "").replace("\r", "").replace(" ", ""))
    materie = tds[3].text[1:]
    tip = tds[4].text[1:]
    profesori = []
    for ref in tds[5].find_all("a"):
        profesori.append(ref.text)
    sala = []
    for ref in tds[6].find_all("a"):
        sala.append(ref.text)
    return [day, ore, grupe, materie, tip, profesori, sala]


def updateExams(exams):
    newExam = {}
    newExam['data'] = exams[0]
    newExam['ora'] = exams[1]
    newExam['materie'] = exams[3]
    newExam['profesori'] = exams[5]
    newExam['sala'] = exams[6]
    newExam['MD5'] = md5(newExam)
    for grupa in exams[2]:
        updateDictionarExams(grupa, newExam)


def parsePagina(url):
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
        parseRow(row, last_day, True)

    global examsList, othersList
    rows = tabel_examene.find_all("tr")
    for row in rows[1:]:
        if len(row.find_all("b")) == 2:
            last_day = ""
            for b in row.find_all("b"):
                last_day = last_day + b.text.replace("\n", "")
            continue
        lista = parseRowExams(row, last_day)
        if lista[4] == "Examen":
            examsList.append(lista)
        else:
            othersList.append(lista)


def updateOthersDictionar(grupa, other):
    global others
    grupe_generale = ['I1', 'I2', 'I3', 'I1B', 'I1A', 'I2A', 'I2B', 'I3A', 'I3B', 'I1E', 'I2E', 'I3E', 'MSD', 'MIS',
                      'MOC', 'MLC']
    if grupa in grupe_generale:
        for myGrupa in others:
            if myGrupa.startswith(grupa):
                deja = False
                for knownOthers in others[myGrupa]:
                    if knownOthers['MD5'] == other['MD5']:
                        deja = True
                        break
                if deja:
                    continue
                others[myGrupa].append(other)
        return
    if grupa not in others:
        others[grupa] = []
    deja = False
    for oldOther in others[grupa]:
        if oldOther['MD5'] == other['MD5']:
            deja = True
            break
    if deja:
        return
    others[grupa].append(other)


def updateOthers(lista):
    newOther = {}
    newOther['data'] = lista[0]
    newOther['ora'] = lista[1]
    newOther['materie'] = lista[3]
    newOther['tip'] = lista[4]
    newOther['profesori'] = lista[5]
    newOther['sala'] = lista[6]
    newOther['MD5'] = md5(newOther)
    for grupa in lista[2]:
        updateOthersDictionar(grupa, newOther)


def crawlOrarFii():
    for pagina in pagini_orar:
        parsePagina(pagina)
        print("Parsed -- {0}".format(pagina))
    global exams, others
    for grupa in orar_grupe:
        exams[grupa] = []
        others[grupa] = []
    for examen_lista in examsList:
        updateExams(examen_lista)
    for others_list in othersList:
        updateOthers(others_list)


def resetFolder(name):
    if os.path.isdir(name):
        rmtree(name)
    os.mkdir(name)


def updateFolders():
    for grupa in orar_grupe:
        path = os.path.join(folderName, grupa)
        resetFolder(path)
        for zi in orar_grupe[grupa]:
            fileName = zi + ".json"
            path = os.path.join(folderName, grupa, fileName)
            handle = open(path, "a+")
            handle.write(json.dumps(orar_grupe[grupa][zi], indent=4, sort_keys=True))
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


def main():
    crawlOrarFii()
    resetFolder(folderName)
    updateFolders()


if __name__ == "__main__":
    main()
