import os

from Models import Anecdote
import sqlite3


class AnecdotesRepository:
    def __init__(self, connection_string):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, connection_string)
        self.connection_string = db_path

    def add(self, anec: Anecdote):
        id = None
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            cursor.execute(
                """
                INSERT INTO Anecdotes
                (text, rating, in_queue)
                VALUES
                (?, ?, ?)
                """, (anec.text, anec.rating, anec.in_queue)
            )

            id = cursor.lastrowid
        return id

    def delete_by_id(self, id):
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            cursor.execute(
                """
                DELETE FROM Anecdotes
                WHERE id = ?
                """, (id,)
            )

    def update(self, anec: Anecdote):
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            cursor.execute(
                """
                INSERT INTO Anecdotes
                (text, rating, in_queue)
                VALUES
                (?, ?, ?)
                WHERE id = ?
                """, (anec.text, anec.rating, anec.in_queue, anec.id)
            )

    def get_by_id(self, id):
        output = None
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            output = cursor.execute(
                """
                SELECT * FROM Anecdotes
                WHERE id = ?
                """, (id,)
            ).fetchall()[0]
        return Anecdote.build_from_tuple(output)