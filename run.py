import json
from forms import ContactForm, csrf, FormTaskCreate, FormTaskUpdate
from flask import Flask, flash, redirect, render_template, request, session, url_for
import platform, sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy(app)

class MyEnum(enum.Enum):
    low = 1
    medium = 2
    high = 3

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created = db.Column(db.Date,default=datetime.utcnow())
    priority = db.Column(db.Enum(MyEnum), default='low')
    is_done = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Task {self.id} {self.title} {self.description} {self.created} {self.priority} {self.is_done}>'

app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf.init_app(app)

def writeJSON(data, filename='dump.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
	data = getData()
	return render_template('index.html', data = data)

@app.route('/about/')
def about():
	data = getData()
	return render_template('about.html', data = data)


skill=["PYTHON",
"HTML/CSS/JS",
"LINUX",
"PHOTOSHOP",
"ADOBE ILLUSTRATOR",
"DaVINCI RESOLVE"]
@app.route('/skills/')
def skills():
	data = getData()
	return render_template('skills.html', len = len(skill), skill = skill, data = data)

@app.route('/contact/',  methods=['GET', 'POST'])
def contact():
	data = getData()
	form = ContactForm()
	isValidName = ""
	isValidEmail = ""
	isValidSubject = ""
	isValidMessage = ""
	if request.method == 'POST':
		if 'name' in session and 'email' in session:
			print(
				f"Name -> {session.get('name')}\nEmail -> {session.get('email')}")
			form.name.data = session.get('name')
			form.email.data = session.get('email')
			if form.validate_on_submit():
				sbj = request.form['subject']
				msg = request.form['message']
				with open('dump.json') as jsonFile:
					data = json.load(jsonFile)
					temp = data['usrMessages']
					temp.append({'Name': form.name.data, 'Email': form.email.data,
								 'Subject': form.subject.data, 'Message': form.message.data})
				writeJSON(data)
				flash(u'Your message has been sent. Thank you!', 'message')
				return redirect(url_for('contact'))
			else:
				flash(u'There were some issues sending the message!', 'error')
		else:
			if form.validate_on_submit():
				usrName = form.name.data
				usrEmail = form.email.data
				sbj = form.subject.data
				msg = form.message.data
				session['name'] = usrName
				session['email'] = usrEmail
				with open('dump.json') as jsonFile:
					data = json.load(jsonFile)
					temp = data['usrMessages']
					temp.append({'Name': form.name.data, 'Email': form.email.data,
								 'Subject': form.subject.data, 'Message': form.message.data})
				writeJSON(data)
				flash(u'Your message has been sent. Thank you!', 'message')
				return redirect(url_for('contact'))
			else:
				flash(u'There were some issues sending the message!', 'error')
	return render_template('contact.html', data = data,
                           form=form,
                           reqMethod=request.method,
                           isValidName=isValidName,
                           isValidEmail=isValidEmail,
                           isValidSubject=isValidSubject,
                           isValidMessage=isValidMessage)


@app.route('/task', methods=["GET", "POST"])
def task():
    data = getData()
    tasks = Task.query.all()
    print(tasks)
    return render_template('tasks.html', title='Список завдань', tasks=tasks, data=data)

@app.route('/task/create', methods=["GET", "POST"])
def task_create():
    data = getData()
    form = FormTaskCreate()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        priority = form.priority.data
        task = Task(title=title, description=description, priority=priority)
        try:
            db.session.add(task)
            db.session.commit()
            # flash('Data added in DB', 'success')
        except:
            db.session.rollback()
            # flash('Error adding data in DB!', 'error')
        return redirect(url_for('task'))
    elif request.method=='POST':
        flash('Unseccess!', 'error')
        return redirect(url_for('task_create'))
    return render_template('task_create.html',  form=form, title='Task create', data=data)

@app.route('/task/<int:id>', methods=["GET", "POST"])
def task_show(id):
    data = getData()
    task = Task.query.get(id)
    return render_template('task_show.html', task=task, data=data)

@app.route('/task/<int:id>/update', methods=["GET", "POST"])
def task_update(id):
    form = FormTaskUpdate()
    task = Task.query.get_or_404(id)
    data = getData()
    if request.method == 'GET': # якщо ми відкрили сторнку для редагування, записуємо у поля форми значення з БД
        form.title.data = task.title
        form.description.data = task.description
        form.created.data = task.created
        form.priority.data = task.priority.name
        form.is_done.data = task.is_done
        return render_template('task_update.html', title='Task Update', form=form, data=data)

    else: # інакше якщо ми змінили дані і натиснули кнопку
        if form.validate_on_submit() or request.method=='POST':
            task.title = form.title.data
            task.description = form.description.data
            task.created = form.created.data
            task.priority = form.priority.data
            task.is_done = form.is_done.data
            try:
                db.session.commit()
                flash('Task seccessfully updated', 'info')
            except:
                db.session.rollback()
                flash('Error while update task!', 'error')
            return redirect(url_for('task'))
        else:
            flash('Error when walidate!', 'error')
            return redirect(f'/task/{id}/update')

@app.route('/task/<int:id>/delete', methods=["GET", "POST"])
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task seccessfully deleted', 'success')
    except:
        flash('Error while delete task!', 'error')
    return redirect(url_for('task'))

def getData():
	now = datetime.now()
	return ["User: " + str(request.headers.get('User-Agent')) , "Platform: " + str(platform.system()) + "Python version:" + str(sys.version_info[0]) + "   Time: " + str(now.strftime("%H:%M:%S"))]


if __name__ == "__main__":
	app.run(debug=True)