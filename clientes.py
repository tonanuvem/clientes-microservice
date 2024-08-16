from datetime import datetime
from flask import jsonify, make_response, abort
from shortuuid import uuid

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") # Local
db = client.clientes

def get_dict_from_mongodb():
    itens_db = db.clientes.find()
    PEOPLE = {}
    for i in itens_db:
            i.pop('_id') # retira id: criado automaticamente 
            item = dict(i)
            PEOPLE[item["id"]] = (i)
    return PEOPLE

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def read_all():
    PEOPLE = get_dict_from_mongodb()
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
    PEOPLE = get_dict_from_mongodb()
    if id in PEOPLE:
        person = PEOPLE.get(id)
    else:
        abort(
            404, "Pessoa com ID {id} nao encontrada".format(id=id)
        )
    return person


def create(person):
    PEOPLE = get_dict_from_mongodb()
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
    item = {
        "id": id,
        "lname": lname,
        "fname": fname,
        "timestamp": get_timestamp(),
    }
    db.clientes.insert_one(item)
    
    PEOPLE = get_dict_from_mongodb()
    return make_response(
        PEOPLE[id],201
        #"Cliente com nome "+fname+" e sobrenome "+lname+" criado com sucesso", 201
    )


def update(id, person):
    query = { "id": id }
    update = { "$set": {
            "id": id,
            "fname": person.get("fname"),
            "lname": person.get("lname"),
            "timestamp": get_timestamp(), } 
        }
    PEOPLE = get_dict_from_mongodb()

    if id in PEOPLE:
        db.clientes.update_one(query, update)
        PEOPLE = get_dict_from_mongodb()

        return PEOPLE[id]
    else:
        abort(
            404, "Pessoa com {id} nao encontrada".format(id=id)
        )

def delete(id):
    query = { "id": id }
    PEOPLE = get_dict_from_mongodb()

    if id in PEOPLE:
        db.clientes.delete_one(query)
        return make_response(
            "{id} deletado com sucesso".format(id=id), 200
        )
    else:
        abort(
            404, "Pessoa com sobrenome {lname} nao encontrada".format(id=id)
        )
