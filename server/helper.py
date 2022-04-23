import sqlite3
from flask import jsonify, url_for
import json

DB_PATH = './data.db'



conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

USERS = 0

c.execute("""
CREATE TABLE IF NOT EXISTS "Users" (
	"id" INTEGER PRIMARY KEY,
	"username" TEXT NOT NULL,
    "avatar" TEXT NOT NULL,
	"sex" TEXT NOT NULL,
	"email" TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS "Stats" (
    "id" INTEGER PRIMARY KEY,
    "total_games" INTEGER,
    "wins" INTEGER,
    "losses" INTEGER,
    "time_spent" INTEGER
)
""")

conn.commit()

def to_json(row):
    result = dict()
    for f in row.keys():
        result[f] = row[f]
    
    return jsonify(result)

def get_user(id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM Users WHERE id=?;', [id])
        res = c.fetchone()

        return to_json(res)
        # return jsonify(res)
    except Exception as e:
        print('Error: ', e)
    return None

def get_all():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM Users')
        res = c.fetchall()
        return res
    except Exception as e:
        print('Error: ', e)
    return None

def add_user(username: str, avatar: str, sex: str , email: str) -> int:
    global USERS
    try:
        id = USERS + 1
        USERS += 1
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('INSERT INTO Users(id, username, avatar, sex, email) VALUES(?,?,?,?,?)', (id, username, avatar, sex, email))
        c.execute('INSERT INTO Stats(id, total_games, wins, losses, time_spent) VALUES (?,?,?,?,?)', (id, 0,0,0,0))
        conn.commit()

        return jsonify({
            'id': id
        })

    except Exception as e:
        print('Error: ', e)
    
    return None


def update_user(id, username: str, avatar: str, sex: str, email: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE Users set username=?, avatar=?, sex=?, email=? WHERE id=?', (username, avatar, sex, email, id))
        conn.commit()

    except Exception as e:
        print('Error: ', e)
    
    return None

def remove_user(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM Users WHERE id=?', [id])
        conn.commit()

    except Exception as e:
        print('Error: ', e)
    
    return None


def get_user_stats(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM Stats WHERE id=?', [id])
        res = c.fetchone()
        return res

    except Exception as e:
        print('Error: ', e)
    
    return None

def update_user_stats(id, total_games, wins, losses, time_spent):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE Stats set total_games=?, wins=?, losses=?, time_spent=? WHERE id=?', (total_games, wins, losses, time_spent,id))
        conn.commit()

    except Exception as e:
        print('Error: ', e)
    
    return None
