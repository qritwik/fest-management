from app import app, render_template, request, url_for, flash, redirect, session
from app.database import retrieve
from operator import itemgetter

r = retrieve()

'''
Login/Logout Process
'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/done', methods = ['GET','POST'])
def done():
	if request.method == "POST":
		uname = request.form['username']
		passw = request.form['password']
		a = r.check_login(uname, passw)
		if a:
			session['username'] = uname
			session['password'] = passw
			if uname == 'admin':
				session['admin'] = 'True'
			return redirect(url_for('home'))
		else:
			render_template('unauthorised.html')
	else:
		return render_template('register.html')


@app.route('/logout')
def logout():
	if 'username' and 'password' in session:
		session.pop('username', None)
		session.pop('password', None)
		session.pop('admin', None)
		return render_template('login.html')
	else:
		return render_template('unauthorised.html')

'''
Login/Logout Ends
'''

@app.route('/')
def home():
	'''
	View Future Events
	'''
	if 'username' and 'password' in session:
		if 'admin' in session:
			admin=True
		else:
			admin=False
		data = r.disp_upcoming_events()
		pop = r.disp_popular_events()[:3]
		upcoming_code = r.get_upcoming_event_code_list()
		print(upcoming_code)
		return render_template('index.html',admin=admin, events = data, header_text="View Upcoming Events", popular=pop, upcoming_code=upcoming_code)
	else:
		return render_template('unauthorised.html')

@app.route('/past-events')
def past_events():
	'''
	View Past Events
	'''
	if 'username' and 'password' in session:
		if 'admin' in session:
			admin=True
		else:
			admin=False
		data = r.disp_past_events()
		upcoming_code = r.get_upcoming_event_code_list()
		return render_template('index.html',admin=admin, events = data,header_text="View Past Events", upcoming_code=upcoming_code)
	else:
		return render_template('unauthorised.html')

@app.route('/events')
def show_event():
	'''
	View detailed information about an event
	'''
	if 'admin' in session:
		admin=True
	else:
		admin=False
	event_footer = r.disp_upcoming_events()
	eid = request.args.get('event')
	data = r.disp_event_details(eid)
	cd = r.get_cname(data[0][7])
	pop = r.disp_popular_events()[:3]
	upcoming_code = r.get_upcoming_event_code_list()
	return render_template('eventDetail.html',admin=admin, events=event_footer, data = data, cd = cd, popular=pop, upcoming_code=upcoming_code)

@app.route('/create-event', methods = ['GET','POST'])
def create_events():
	'''
	Create Events
	'''
	if 'admin' in session:
		admin=True
	else:
		admin=False
	if request.method == "GET":
		if 'username' and 'password' and 'admin' in session:
			event_footer = r.disp_upcoming_events()
			upcoming_code = r.get_upcoming_event_code_list()
			return render_template('create_event.html',admin=admin,events=event_footer, upcoming_code=upcoming_code)
		else:
			return render_template('unauthorised.html')
	if request.method == "POST":
		if 'username' and 'password' in session:
			event_code = request.form['event_code']
			title = request.form['title']
			date = request.form['date']
			desc = request.form['desc']
			venue = request.form['venue']
			price = request.form['price']
			cord = request.form['coordinator']
			a = r.insert_event(event_code, title, date, desc, venue, price, 'static/event-images/code.jpg', cord)
			return redirect(url_for('home'))
		else:
			return render_template('unauthorised.html')


@app.route('/delete-event', methods=['GET', 'POST'])
def delete_event():
	if 'admin' in session:
		admin=True
	else:
		admin=False
	if request.method == "GET":
		event_footer = r.disp_upcoming_events()
		eid = request.args.get('event')
		data = r.disp_event_details(eid)
		cd = r.get_cname(data[0][7])
		pop = r.disp_popular_events()[:3]
		upcoming_code = r.get_upcoming_event_code_list()
		return render_template('eventdelete.html',admin=admin, events=event_footer, data = data, cd = cd, popular=pop, upcoming_code=upcoming_code)
	if request.method == "POST":
		event_id = request.form['yes']
		r.del_event(event_id)
		return redirect(url_for('home'))


@app.route('/insert-winner', methods = ['GET','POST'])
def insert_winner():
	'''
	Add users to winners list
	'''
	if request.method == "POST":
		if 'username' and 'password' in session:
			event_id = request.form['event']
			user_id = request.form['name']
			rank = request.form['rank']
			a = r.insert_win_details(event_id, user_id, rank)
			return redirect(url_for('insert_winner'))
		else:
			return render_template('unauthorised.html')
	if request.method == "GET":
		if 'username' and 'password' in session:
			if 'admin' in session:
				admin=True
			else:
				admin=False
			event_list = r.get_all_events()
			name_list = r.get_all_users()
			upcoming_code = r.get_upcoming_event_code_list()
			event_footer = r.disp_upcoming_events()
			return render_template('winner-entry.html', admin=admin, names=name_list, events=event_list, upcoming_code=upcoming_code)
		else:
			return render_template('unauthorised.html')


@app.route('/winners')
def show_winners():
	'''
	Show event winners
	'''
	names= {}
	if 'username' and 'password' in session:
		if 'admin' in session:
			admin=True
		else:
			admin=False
		event = str(request.args.get('event'))
		data = r.disp_win_details(event)
		print('a: ' + str(data))
		for i in data:
			a = r.get_user_name(str(i[1]))
			print(a)
			names[a] = i[2]
		event_name = r.disp_event_details(event)[0][1]
		print(data)
		print(names)
		upcoming_code = r.get_upcoming_event_code_list()
		event_footer = r.disp_upcoming_events()
		return render_template('winners.html',admin=admin, events=event_footer, data=names, event_name = event_name, upcoming_code=upcoming_code)
	else:
	 	return render_template('unauthorised.html')
	# else:
	# 	return render_template('unauthorised.html')
	# 	event_id = '1'
	# 	a = r.disp_win_details(event_id)
	# 	# for i in a:
	# 	# 	b = r.get_user_name(str(i[2]))
	# 	# 	a[0].append(b)
	# 	upcoming_code = r.get_upcoming_event_code_list()
	# 	event_footer = r.disp_upcoming_events()
	# 	return render_template('winners.html',admin=admin, events=event_footer, people = a, upcoming_code=upcoming_code)
	# else:
	# 	return render_template('unauthorised.html')

# @app.route('/show-winners')
# def show_winners():
# 	a = r.show_win_details()
# 	return render_template('show-winners.html',data=a)

@app.route('/register', methods = ['GET','POST'])
def register():
	'''
	Register for Events
	'''
	if 'username' and 'password' in session:
		if 'admin' in session:
			admin=True
		else:
			admin=False
		if request.method == "GET":
			ev = r.get_all_events()
			return render_template('register.html', events = ev)
		if request.method == "POST":
			event_id = request.form['event']
			user_id = r.get_user_id(session['username'])
			number = request.form['number']
			print(event_id)
			print(user_id)
			print(number)
			a = r.insert_register(event_id, user_id, number)
			upcoming_code = r.get_upcoming_event_code_list()
			event_footer = r.disp_upcoming_events()
			return render_template('index.html',admin=admin, events=event_footer, upcoming_code=upcoming_code)
	else:
		return render_template('unauthorised.html')


@app.route('/registrations')
def registrations():
	'''
	View Event Registrations
	'''
	names = {}
	if 'username' and 'password' in session:
		if 'admin' in session:
			admin=True
		else:
			admin=False
		event = str(request.args.get('event'))
		data = r.get_all_registered(event)
		for i in data:
			a = r.get_user_name(str(i[1]))
			print(a)
			names[a] = i[2]
		event_name = r.disp_event_details(event)[0][1]
		print(data)
		print(names)
		upcoming_code = r.get_upcoming_event_code_list()
		event_footer = r.disp_upcoming_events()
		return render_template('registrations.html',admin=admin, events=event_footer, data=names, event_name = event_name, upcoming_code=upcoming_code)
	else:
		return render_template('unauthorised.html')
