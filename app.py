from flask import Flask, render_template, jsonify, request, redirect, url_for
from dotenv import load_dotenv

from config import Config
from flask_sqlalchemy import SQLAlchemy

from forms import TaskForm


load_dotenv("./.flaskenv")


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

import models


@app.route("/")
def index():
    tasks = models.Task.query.all()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(tasks)
    
    return render_template("index.html")


@app.route('/create', methods=['POST'])
def create_task():
    user_input = request.get_json()
    form = TaskForm(data=user_input)

    if form.validate():
        task = models.Task(title=form.title.data)
        db.session.add(task)
        db.session.commit()
        return jsonify(task)
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.get_json().get('id')
    task = models.Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': 'Ok'}, 200)


@app.route('/toggle-state', methods=['POST'])
def complete_task():
    task_id = request.get_json().get('id')
    task = models.Task.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    db.session.add(task)
    db.session.commit()
    return jsonify({'result': 'Ok'}, 200)


if __name__ == "__main__":
    app.run()