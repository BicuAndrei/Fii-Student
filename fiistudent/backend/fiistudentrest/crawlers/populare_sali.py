from fiistudentrest.models import Classroom

def populate_datastore():
    sali = ['Acvariu', 'C210', 'C401', 'C403', 'C405', 'C409', 'C411', 'C412', 'C413', 'C112', 'C114', 'C2', 'C309',
            'C308', 'C901', 'C903', 'C905', 'C909']
    capacitati = [20, 30, 30, 30, 30, 30, 30, 30, 30, 120, 0, 200, 100, 60, 15, 30, 30, 30]
    capacitate = 0
    for sala in sali:
        if sala=='Acvariu':
            etaj = 1
        else:
            etaj = int(sala[1]) - 2

        if sala in ['C309','C308','C112']:
            type='sala de curs'
        elif sala == 'C2':
            type='amfiteatru'
        elif sala[1] in [4] or sala in ['C210']:
            type = 'laborator'
        elif sala == 'Acvariu':
            type='alte sali'
        else:
            type = 'sala de seminar'

        classroom = Classroom(
            floor = int(etaj),
            identifier = sala,
            capacity = int(capacitati[capacitate]),
            type = type
        )

        capacitate = capacitate + 1

        classroom.put()


def remove_existing_entities():
    classroom = Classroom(
        floor=1,
        type='-',
        capacity=0,
        identifier='-'
    )
    classrooms = classroom.query().fetch()
    for c in classrooms:
        c.remove()


def main():
    remove_existing_entities()
    populate_datastore()
    classroom = Classroom(
        floor=0,
        type='alte sali',
        capacity=30,
        identifier='B5'
    )
    classroom.put()
    classroom = Classroom(
        floor=0,
        type='cabinet',
        capacity=0,
        identifier='Cabinet'
    )
    classroom.put()


if __name__ == '__main__':
    main()
