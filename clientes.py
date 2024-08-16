from datetime import datetime
from flask import jsonify, make_response, abort
from shortuuid import uuid

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

id1, id2, id3 = str(uuid()), str(uuid()), str(uuid())

PEOPLE = {
    id1: {
        "id": id1,
        "fname": "Indiana",
        "lname": "Jones",
        "timestamp": get_timestamp(),
    },
    id2: {
        "id": id2,
        "fname": "Jack",
        "lname": "Sparrow",
        "timestamp": get_timestamp(),
    },
    id3: {
        "id": id3,
        "fname": "John",
        "lname": "Snow",
        "timestamp": get_timestamp(),
    },
}

def read_all():
    dict_clientes = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
    clientes = jsonify(dict_clientes)
    qtd = len(dict_clientes)
    content_range = "clientes 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    clientes.headers['Access-Control-Allow-Origin'] = '*'
    clientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    clientes.headers['Content-Range'] = content_range
    return clientes

def read_one(id):
    if id in PEOPLE:
        person = PEOPLE.get(id)
    else:
        abort(
            404, "Pessoa com ID {id} nao encontrada".format(id=id)
        )
    return person


def create(person):
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    for id in PEOPLE:
        if fname == PEOPLE[id]["fname"] and lname == PEOPLE[id]["lname"]:            
            # Cliente já existe
            abort(
                406,
                "Pessoa com nome "+fname+" e sobrenome "+lname+" ja existe"
            )
        else:
            continue
    
    # Cliente nao existe, pode CRIAR:
    id=str(uuid())
    PEOPLE[id] = {
        "id": id,
        "lname": lname,
        "fname": fname,
        "timestamp": get_timestamp(),
    }
    return make_response(
        PEOPLE[id],201
        #"Cliente com nome "+fname+" e sobrenome "+lname+" criado com sucesso", 201
    )


def update(id, person):
    if id in PEOPLE:
        PEOPLE[id]["fname"] = person.get("fname")
        PEOPLE[id]["lname"] = person.get("lname")
        PEOPLE[id]["timestamp"] = get_timestamp()

        return PEOPLE[id]
    else:
        abort(
            404, "Pessoa com {id} nao encontrada".format(id=id)
        )

def delete(id):
    if id in PEOPLE:
        del PEOPLE[id]
        return make_response(
            "{id} deletado com sucesso".format(id=id), 200
        )
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(id=id)
        )

