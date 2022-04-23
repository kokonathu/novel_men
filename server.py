from sqlite3.dbapi2 import connect
import time as t
import json
import sqlite3

from flask import Flask, render_template, request, Response

app = Flask(__name__, static_folder="public")


@app.route("/")
def serve_route():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute("select title from todo")
    raw_tasks = cursor.fetchall()

    tasks = [mytask[0] for mytask in raw_tasks]

    return render_template("main.html", tasks=tasks)


@app.route("/register/", methods=["POST", ])
def api_register():
    req_data = json.loads(request.data.decode(request.charset))

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "insert into todo values (:time, :title, :detail)",
        {
            "time": t.time(),
            "title": req_data["title"],
            "detail": "detail"
        }
    )

    conn.commit()

    return Response(status=200)


if __name__ == "__main__":

    # Tableだけ作る
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    cursor.execute(
        "create table if not exists todo("
        "time integer, "
        "title text,"
        "detail title"
        ")"
    )
    conn.commit()
    conn.close()

    app.run(host="0.0.0.0", debug=True, port=3000, )
