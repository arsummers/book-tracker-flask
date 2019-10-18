from datetime import datetime
from flask import make_response, abort

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}

def read_all():
    """
    creates list of all people
    """
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]

def read_one(lname):
    """
    searches through list of people based on name
    """
    if lname in PEOPLE:
        person = PEOPLE.get(lname)

    else:
        abort(
            404, "Last name {lname} not found".format(lname=lname)
        )
    
    return person

def create(person):
    """
    creates a new person object in the PEOPLE structure based on data that is passed in
    """

    lname = person.get('lname', None)
    fname = person.get('fname', None)

    # checks if person already exists
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            'lname':lname,
            'fname':fname,
            'timestamp':get_timestamp()
        }
        return make_response(
            '{lname} successfully created.'.format(lname=lname), 201
        )

    else:
        abort(
            406,
            'Person with last name {lname} already exists'.format(lname=lname)
        )

def update(lname, person):
    """
    updates and existing person
    """
    if lname in PEOPLE:
        PEOPLE[lname]['fname'] = person.get('fname')
        PEOPLE[lname]['timestamp'] = get_timestamp()

        return PEOPLE[lname]

    else:
        abort(
            404,
            "Person with name {lname} not found".format(lname=lname)
        )

def delete(lname):
    """
    yeets a person from the structure
    """
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successsfully deleted".format(lname=lname), 200
        )

    else:
        abort(
            404,
            "Person with name {lname} not found".format(lname=lname)
        )