from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Task: {self.id}'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        currentTask = request.form['content']
        newTask = myTask(content = currentTask)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error: {e}')
            return f'Error: {e}'
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'ERROR: {e}'
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    task = myTask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error: {e}'
    else:
        return 'HOME'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)


