import sqlite3
import time

class ScoreManager():

    _requests = {
        "_create" : "CREATE TABLE IF NOT EXISTS history (date INTEGER, score INTEGER)",
        "_add_score" : "INSERT INTO history (date, score) VALUES (?, ?)",
        "_best_score" : "SELECT MAX(score) FROM history"
    }

    def __init__(self):

        with sqlite3.connect('db/score.db') as db:
            cursor = db.cursor()
            cursor.execute(self._requests["_create"])
    
    def save_score(self, game_score=0):
        with sqlite3.connect('db/score.db') as db:
            if game_score > 0:
                cursor = db.cursor()
                cursor.execute(self._requests["_add_score"], (time.time(), game_score))
                db.commit()

    def find_best_score(self):
        with sqlite3.connect('db/score.db') as db:
            cursor = db.cursor()
            cursor.execute(self._requests["_best_score"])
            result = cursor.fetchone()
            return result[0] if result else 0
        