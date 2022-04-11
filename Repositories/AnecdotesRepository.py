import os

from Models import Anecdote
import sqlite3


class RandomMethods:
    ALL = 0
    VERIFIED = 1
    UNVERIFIED = 2


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

    def get_random_verified(self):
        return self.get_random(RandomMethods.VERIFIED)

    def get_random_unverified(self):
        return self.get_random(RandomMethods.UNVERIFIED)

    def get_random(self, method=RandomMethods.ALL):
        search_adding = ""

        if method == RandomMethods.VERIFIED:
            search_adding = "AND in_queue = 1;"
        elif method == RandomMethods.UNVERIFIED:
            search_adding = "AND in_queue = 0;"

        output = None
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            while output is None:
                output = cursor.execute(
                    f"""
                    SELECT * FROM Anecdotes
                    WHERE rowid = (ABS(random()) % (SELECT (SELECT MAX(rowid) FROM Anecdotes)+1))
                    {search_adding}
                    """
                ).fetchall()
                if len(output) == 0:
                    output = None
            output = output[0]
        return Anecdote.build_from_tuple(output)

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

    def submit_anec_by_id(self, id):
        with sqlite3.connect(self.connection_string) as con:
            cursor = con.cursor()

            cursor.execute(
                """
                UPDATE Anecdotes
                SET in_queue = 1
                WHERE id = ?
                """, (id,)
            )