from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks
# A list of dictionaries, where each dictionary represents a task
tasks = [
    {'id': 1, 'content': 'タスク管理ツールを作成する', 'done': False},
    {'id': 2, 'content': 'Flaskを勉強する', 'done': True}
]
# To keep track of the next task id
next_id = 3

@app.route('/', methods=['GET', 'POST'])
def index():
    global next_id
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content: # Ensure content is not empty
            tasks.append({'id': next_id, 'content': task_content, 'done': False})
            next_id += 1
        return redirect(url_for('index'))
    # Sort tasks to show undone tasks first
    sorted_tasks = sorted(tasks, key=lambda x: x['done'])
    return render_template('index.html', tasks=sorted_tasks)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Using host='0.0.0.0' to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
