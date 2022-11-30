import os
from datetime import timedelta
import secrets


import pandas as pd
from flask import Flask, render_template, request, url_for, redirect, session, send_file

from users import User
from paid import Paid
from amb import Amb
from committee import Committee
from contacts import Contacts
from config import *


app = Flask(__name__)
app.secret_key = "........"
app.permanent_session_lifetime = timedelta(minutes=120)

users = User()
paid_ = Paid()
ambs = Amb()
comm = Committee()
cont = Contacts()


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if 'user' in session:
		return redirect(url_for('dashboard'))

	else:
		if request.method == 'POST':
			session.permanent = True
			name = request.form['name']
			std = request.form['std']
			school = request.form['school']

			email = request.form['email']
			ph1 = request.form['ph1']
			ph2 = request.form['ph2']
			
			prc1 = request.form['prc1']
			prp1 = request.form['prp1']
			prc2 = request.form['prc2']
			prp2 = request.form['prp2']
			prc3 = request.form['prc3']
			prp3 = request.form['prp3']
			
			exp = request.form['exp']
			fp = request.form['fp']
		
			amb_ = request.form['amb']
			accom = request.form['acomm']
			notes = request.form['notes']
			
			paid=0
			emailed=0
			secret = secrets.token_urlsafe(4)

			users.data_entry(name,std,school,exp,fp,notes, paid, secret, accom)
			ambs.data_entry(name, amb_, secret)
			comm.data_entry(name, prc1, prc2, prc3, prp1, prp2, prp3, secret)
			cont.data_entry(emailed, name, email, ph1, ph2, secret)


			return redirect(url_for('dashboard'))


		else:
			return render_template('register.html')



@app.route('/pop')
def pop():
	if 'user' in session:
		session.pop('user')
		return redirect(url_for('register'))

	else:
		return redirect(url_for('register'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	if 'admin' in session:
		return redirect(url_for('admin'))

	else:
		if request.method=='POST':
			usr = request.form['username']
			passw = request.form['password']

			if passw==pw_admin and usr=='shakhyar' or usr=='parikhit' or usr=='murtaza' or usr=='iku':
				session['admin'] = 'usr'
				return redirect(url_for('admin'))

			else:
				return render_template('admin_login.html', msg='Wrong password')

		else:
			return render_template('admin_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "reject":
				secret = action[action.index(':')+1:]
				print(secret)
				users.delete_entry(secret)
				ambs.delete_entry(secret)
				comm.delete_entry(secret)
				cont.delete_entry(secret)
				paid_.delete_entry(secret)
				return redirect(url_for('admin'))

			elif flag == "paid":
				# extracts the information of the given pid, redirects to profit page, and returns to dashboard
				secret = action[action.index(':')+1:]
				users.update_entry(secret)
				print(secret)
				return redirect(url_for('admin'))


		else:
			all_list = users.read_all()
			length = len(all_list)
			"""d = users.count_disec()
			a = users.count_aippm()
			n = users.count_neppm()
			i = users.count_ipc()"""
			up = len(users.read_unpaid())
			pd = len(paid_.read_all())
			total = pd*250
			return render_template('admin.html', l=all_list, size=length, up=up, pd=pd, total=total)
	else:
		return redirect(url_for('admin_login'))


@app.route('/admin-logout')
def admin_logout():
	if 'admin' in session:
		session.pop('admin')
		return redirect(url_for('admin_login'))
	else:
		return redirect(url_for('admin_login'))

@app.route('/payments', methods=['GET', 'POST'])
def payments():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "paid":
				secret = action[action.index(':')+1:]
				print(secret)
				users.update_entry(secret)
				name = users.read_sec(secret)
				paid_.data_entry(name, secret)
				return redirect(url_for('payments'))


			elif flag=='resurrection':
				secret = action[action.index(':')+1:]
				paid_entries = users.paid_check()

				for _paid in paid_entries:
					paid_.data_entry(_paid[0], _paid[-2])

				return redirect(url_for('payments'))


			else:
				return redirect(url_for('payments'))

		else:
			all_list = users.read_unpaid()
			leng = len(all_list)
			return render_template('payments.html', l=all_list, num=leng)

	else:
		return redirect(url_for('admin_login'))


@app.route('/paid', methods=['GET', 'POST'])
def paid():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			print(flag, action)


			if flag=='delete':
				secret = action[action.index(':')+1:]
				paid_.delete_entry(secret)
				return redirect(url_for('paid'))
			else:
				return redirect(url_for('paid'))

		else:
			all_list = paid_.read_all()
			leng = len(all_list)
			return render_template('paid.html', l=all_list, num=leng)


	else:
		return redirect(url_for('admin_login'))

@app.route('/download')
def download():
	if 'admin' in session:
		try:
			os.remove(r'E:\smmsmun22\site\static\data.csv')
		except Exception as e:
			print(e)
		l = users.read_all()
		df = pd.DataFrame((l), columns =['Name','Standard','School','exp','fp','notes','paid','secret', 'Accommodation'])

		df.to_csv(csv_path)

		return send_file(csv_path, as_attachment=True)
	else:
		return redirect(url_for('admin_login'))

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/change/<token>', methods=['GET', 'POST'])
def change(token):
	if 'user' in session:
		if request.method == 'POST':
			com = request.form['prc']
			users.update_prc(token, com)
			return redirect(url_for('dashboard'))

		else:
			return render_template('change.html')

	else:
		return redirect(url_for('login'))



@app.route('/more-downloads', methods=['GET', 'POST'])
def more_downloads():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]
			secret = action[action.index(':')+1:action.index('-')]
			coms = action[action.index('-')+1:]



			down = comm.parse_download(flag, secret, coms)

			try:
				os.remove(r'E:\smmsmun22\site\static\data.csv')
			except Exception as e:
				print(e)
				df = pd.DataFrame((down), columns =['Name', 'Portfolio'])

				down_path = f"{BASE}{secret}-{flag}.csv"
				df.to_csv(down_path)

			return send_file(down_path, as_attachment=True)
		
		else:	
			return render_template('more-downloads.html')

	else:
		return redirect(url_for('admin_login'))




@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "reject":
				secret = action[action.index(':')+1:]
				print(secret)
				cont.update_entry(secret)
				return redirect(url_for('contacts'))

			else:
				return redirect(url_for('contacts'))

		else:
			all_list = cont.read_all()
			return render_template('contacts.html', l=all_list)

	else:
		return redirect(url_for('admin_login'))



@app.route('/amb', methods=['GET', 'POST'])
def _amb():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "reject":
				secret = action[action.index(':')+1:]
				print(secret)
				cont.update_entry(secret)
				return redirect(url_for('_amb'))

			else:
				return redirect(url_for('_amb'))

		else:
			all_list = ambs.read_all()
			return render_template('amb.html', l=all_list)

	else:
		return redirect(url_for('admin_login'))



########################################################
"""@app.route('/com-downloads', methods=['GET', 'POST'])
def com_downloads():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]
			secret = action[action.index(':')+1:]
			coms = action[action.index('=')+1:]

			down = comm.parse_download(flag, secret, coms)

			try:
				os.remove(r'E:\smmsmun22\site\static\data.csv')
			except Exception as e:
				print(e)
				df = pd.DataFrame((down), columns =['Name', 'Portfolio'])

				down_path = f"{BASE}{secret}-{flag}.csv"
				df.to_csv(down_path)

			return send_file(down_path, as_attachment=True)

			#if flag == "prc1": #prc1, elif prc2....
				secret = action[action.index(':')+1:]
				print(secret)
				contacts.update_entry(secret)
				return redirect(url_for('contacts'))

			elif flag == "prc2": #prc1, elif prc2....
				secret = action[action.index(':')+1:]
				print(secret)
				contacts.update_entry(secret)
				return redirect(url_for('contacts'))

			elif flag == "prc3": #prc1, elif prc2....
				secret = action[action.index(':')+1:]
				print(secret)
				contacts.update_entry(secret)
				return redirect(url_for('contacts'))

			else:
				return redirect(url_for('contacts'))#

		else:
			return render_template('more-downloads.html')

	else:
		return redirect(url_for('admin_login'))"""

#########################################################
@app.route('/committee')
def committee():
	if 'admin' in session:
		all_list = comm.read_all()
		unsc = comm.count_unsc()
		ds = comm.count_disec()
		lk = comm.count_loksabha()
		abs_ = comm.count_abs()
		ipc = comm.count_ipc()

		unsc1 = comm.unsc1()
		ds1 = comm.ds1()
		lk1 = comm.lk1()
		abs1 = comm.abs1()
		ipc1 = comm.ipc1()


		try:
			unscp = round((unsc/(unsc+ds+lk+abs_+ipc))*100, 2)
			dsp = round((ds/(unsc+ds+lk+abs_+ipc))*100, 2)
			lkp = round((lk/(unsc+ds+lk+abs_+ipc))*100, 2)
			absp = round((abs_/(unsc+ds+lk+abs_+ipc))*100, 2)
			ipcp = round((ipc/(unsc+ds+lk+abs_+ipc))*100, 2)

		except Exception as e:
			print(e)
			unscp = round((unsc/1)*100, 2)
			dsp = round((ds/1)*100, 2)
			lkp = round((lk/1)*100, 2)
			absp = round((abs_/1)*100, 2)
			ipcp = round((ipc/1)*100, 2)

		return render_template('committee.html', l=all_list, t=len(all_list), unsc=unsc, ds=ds, lk=lk, abs_ = abs_, ipc=ipc,
			unsc1=unsc1, ds1=ds1, lk1=lk1, abs1=abs1, ipc1=ipc1, unscp=unscp, dsp=dsp, lkp=lkp, absp=absp, ipcp=ipcp)
	else:
		return redirect(url_for('admin_login'))


if __name__ == '__main__':
	app.run(debug=True)