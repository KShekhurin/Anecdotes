import psycopg2

from Models import Anecdote
import sqlite3



class RandomMethods:
    ALL = 0
    VERIFIED = 1
    UNVERIFIED = 2


class AnecdotesRepositoryPost:
    def __init__(self, connection):
        self.connection = connection
    
    def add(self, anec: Anecdote):
        id = None
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO "Anecdote"
                (text, in_queue)
                VALUES
                (%s, %s)
                """, (anec.text, anec.in_queue)
            )

            id = cursor.lastrowid
        return id

    def delete_by_id(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM "Anecdote"
                WHERE id = %s
                """, (id,)
            )

    def update(self, anec: Anecdote):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO "Anecdote"
                (text, in_queue)
                VALUES
                (%s, %s)
                WHERE id = %s
                """, (anec.text, anec.in_queue, anec.id)
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
        with self.connection.cursor() as cursor:
            while output is None:
                cursor.execute(
                    f"""
                    select * from "Anecdote"
                    {search_adding}
                    ORDER BY random() limit 1
                    """
                )
                output = cursor.fetchall()
                if len(output) == 0:
                    output = None
            output = output[0]
        return Anecdote.build_from_tuple(output)

    def get_by_id(self, id):
        output = None
        with self.connection.cursor() as cursor:
            output = cursor.execute(
                """
                SELECT * FROM "Anecdote"
                WHERE id = %s
                """, (id,)
            ).fetchall()[0]
        return Anecdote.build_from_tuple(output)

    def submit_anec_by_id(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE "Anecdote"
                SET in_queue = 1
                WHERE id = %s
                """, (id,)
            )