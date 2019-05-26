from fiistudentrest.models import Professor

diac_conv = {"Ă": "A", "ă": "a", "Â": "A", "â": "a", "Î": "I", "î": "i", "Ș": "S", "ș": "s", "Ț": "T", "ț": "t",
             "ş": "s", "Ş": "S"}


def main():
    all_profs = Professor.all()
    for prof in all_profs:
        prof.remove()
        for letter in diac_conv:
            if letter in prof.firstName:
                prof.firstName = prof.firstName.replace(letter, diac_conv[letter])
            if letter in prof.lastName:
                prof.lastName = prof.lastName.replace(letter, diac_conv[letter])
        prof.put()


if __name__ == "__main__":
    main()
