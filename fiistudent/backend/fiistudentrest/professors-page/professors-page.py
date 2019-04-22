import hug
import json

from fiistudentrest.models import Professor


@hug.local()
@hug.get()
@hug.cli()
def professors():
    professors_list = []
    teached_subjects = []

    professors_query = Professor.query()
    professors_query_it = professors_query.fetch()

    for ent in professors_query_it:
        dictionary = {}
        dictionary["id"] = ent.urlsafe
        name = ent.firstName
        name += " " + ent.lastName
        dictionary["name"] = name
        dictionary["title"] = ent.type
        dictionary["office"] = ent.office
        dictionary["link"] = ent.link
        dictionary["teachedSubjects"] = teached_subjects

        professors_list.append(dictionary)

    json_data = json.dumps(professors_list)
    return json_data
