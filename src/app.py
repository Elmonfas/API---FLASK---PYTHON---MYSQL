from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:elmonfas@localhost/flask_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))  
    
    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

## Ruta de CREATE QUE ES POST
@app.route('/tasks', methods=['POST'])
def create_task():

    # print(request.json)
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title,description)
    print('Tarea creada maboy')

    db.session.add(new_task)
    db.session.commit()
    print('Almacenamiento en la base de datos --> OK!')


    return task_schema.jsonify(new_task)

## Ruta de READ ALL tasks - GET
@app.route('/tasks', methods=['GET'])
def get_tasks():
    ## Nos devuelve todas las tareas
    all_tasks = Task.query.all()
    ## Lista con los datos
    result = tasks_schema.dump(all_tasks)
    ## Convertimos en JSON los resultados del select de la base de datos por el ORM.
    return jsonify(result)

## Ruta READ Single task - GET
@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)

    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.session.get(Task, id)
    title = request.json['title']
    description = request.json['description']
    print(title, description)

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)


@app.route('/tasks/<id>', methods=['DELETE'])
def del_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

## Ruta landing page - PAGINA DE INICIO /
@app.route('/', methods=['GET'])
def index():

    return jsonify({'message':'Welcome to my first API with Python Flask and MYSQL'})

@app.route('/tasks/delete', methods=['DELETE'])
def delete_tasks():
    db.session.query(Task).delete()
    db.session.commit()
    return jsonify({"message":"All tasks deleted!!!"})

if __name__ == '__main__':
    app.run(debug=True)
