from flask import request

from main import app
from Repositories import AnecdotesRepository
from Models import Anecdote


anecdote_repository = AnecdotesRepository("../db.db")


@app.route("/anecdote/<int:id>", methods=["GET"])
def get_anecdote_by_id(id):
    anec = anecdote_repository.get_by_id(id)

    if anec is None:
        return "There is no such a id", 404

    return anec.toJSON(), 200, {'Content-Type': 'text/json; charset=utf-8'}


@app.route("/anecdote/rand", methods=["GET"])
def get_random_anecdote():
    anec = anecdote_repository.get_random()
    return anec.toJSON(), 200, {'Content-Type': 'text/json; charset=utf-8'}


@app.route("/anecdote/", methods=["PUT"])
def update_in_list():
    pass


@app.route("/anecdote/", methods=["POST"])
def add_to_list():
    data = request.json

    if "text" not in data.keys():
        return "There is no text in body", 403

    anec = Anecdote(
        text=data["text"],
    )
    anecdote_repository.add(anec)

    return "Ok", 200


@app.route("/anecdote/<int:id>", methods=["DELETE"])
def delete_from_list_by_id(id):
    anecdote_repository.delete_by_id(id)
    return "", 200
