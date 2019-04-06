from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'Prem':
        return 'password'
    return None

@auth.error_handler
def unorthorized():
    return make_response(jsonify({'error':'unorthorized access'}), 401)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required  # add this to routes that you want authentication before displaying API response
def get_tasks():
#    return jsonify({'all tasks': tasks})

    # to return the URI that controls the tasks
    # helps users construct the request.
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})
# pass username and password to access get_tasks()
# curl -u Prem:password -i http://localhost:5000/todo/api/v1.0/tasks
    


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task {}'.format(task_id): task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description',""),
            'done': False
            }
    tasks.append(task)
    return jsonify({'tasks': tasks}), 201 # 201 is CREATED status code
# use this command to call:  
# curl -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"Read a book\"}"
# http://localhost:5000/todo/api/v1.0/tasks
# or  "{"""title""":"""Read a book"""}"


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    
    # check if json present in update request
    if not request.json:
        abort(400) # Bad Request
    
    task = [task for task in tasks if task['id'] == task_id]
    
    # check if task to be updated is present
    if len(task) == 0:
        abort(404) # Not found
    
    # if 'title' present in change request json, then check to see if it is string
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    
    # if 'description' present in change request json, then check to see if it is string
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    
    # if 'done' present in change request json, then check to see if it is string
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    
    return jsonify({"updated task":task[0]})
# use the following command to run:
# curl -i -H "Content-Type: application/json" -X PUT -d "{\"done\":true}" http://localhost:5000/todo/api/v1.0/tasks/2



@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    
    if len(task) == 0:
        abort(404)
    
    tasks.remove(task[0])
    return jsonify({"result": True})
# to delete, use this command:
# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/todo/api/v1.0/tasks/<task_id>



@app.errorhandler(404)
def error_handler(e):
    return make_response(jsonify({"Error": "Not Found"}),404)



if __name__ == '__main__':
    app.run(debug=True)