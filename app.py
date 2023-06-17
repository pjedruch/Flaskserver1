from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# instantiate flask app
app = Flask(__name__)
ma = Marshmallow(app)

# set configs
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

# instatiate db object
db = SQLAlchemy(app)


# create database
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    timeout = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.id


# create Todolist schema
class TodoListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'timeout')


# create instance of schema
todolist_schema = TodoListSchema(many=False)
todolists_schema = TodoListSchema(many=True)


# create todos route
@app.route('/sites', methods=["POST"])
def add_todo():
    try:
        name = request.json['name']
        timeout = request.json['timeout']

        new_todo = TodoList(name=name, timeout=timeout)

        db.session.add(new_todo)
        db.session.commit()

        return todolist_schema.jsonify(new_todo)
    except Exception as e:
        return jsonify({"Error": "Invalid request."})


# get sites
@app.route('/sites', methods=["GET"])
def get_todos():
    todos = TodoList.query.all()
    result_set = todolists_schema.dump(todos)
    return jsonify(result_set)


# get todo by id
@app.route('/sites/<int:id>', methods=["GET"])
def get_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    return todolist_schema.jsonify(todo)


# update todo
@app.route('/sites/<int:id>', methods=["PUT"])
def update_todo(id):
    todo = TodoList.query.get_or_404(int(id))

    name = request.json['name']
    timeout = request.json['timeout']

    todo.name = name
    todo.timeout = timeout

    db.session.commit()

    return todolist_schema.jsonify(todo)


# delete todo
@app.route('/sites/<int:id>', methods=["DELETE"])
def delete_todo(id):
    todo = TodoList.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"Succes": "Todo deleted."})



@app.route('/')
def todo():
    return jsonify({"MSG": "Hello world from API"})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
