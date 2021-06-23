import json
from forms import ContactForm, csrf
from flask import Flask, flash, redirect, render_template, request, session, url_for
import platform, sys
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
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

def getData():
	now = datetime.now()
	return ["User: " + str(request.headers.get('User-Agent')) , "Platform: " + str(platform.system()) + "Python version:" + str(sys.version_info[0]) + "   Time: " + str(now.strftime("%H:%M:%S"))]


if __name__ == "__main__":
	app.run(debug=True)