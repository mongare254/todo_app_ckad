from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Todo

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Home (View)
@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')

    if content:
        new_task = Todo(content=content)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('index'))

# Toggle complete
@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)