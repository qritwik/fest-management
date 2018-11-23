from flask import Flask
from flaskext.mysql import MySQL

from passlib.hash import django_pbkdf2_sha256

app = Flask('__main__')
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'event_management'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

class retrieve:
    'sql querries'

    def get_all_users(self):
        cursor.execute("SELECT * FROM auth_user ")
        data = cursor.fetchall()
        return(data)

    def get_all_events(self):
        cursor.execute("SELECT * FROM event ")
        data = cursor.fetchall()
        return(data)

    def get_all_registered(self, event_id):
        cursor.execute("SELECT * FROM registrations WHERE event_id='" + event_id + "' ")
        data = cursor.fetchall()
        return(data)

    def get_user_id(self, uname):
        cursor.execute("SELECT id FROM auth_user WHERE username = '" + uname + "' ")
        data = cursor.fetchall()[0][0]
        return(data)

    def get_user_name(self, uid):
        cursor.execute("SELECT username FROM auth_user WHERE id = '"+uid+"'")
        data = cursor.fetchall()
        return(data)

    def disp_upcoming_events(self):
        cursor.execute("SELECT * FROM event WHERE date >= NOW()")
        data = cursor.fetchall()
        return(data)

    def disp_popular_events(self):
        cursor.execute("SELECT * FROM event WHERE date >= NOW() order by price ")
        data = cursor.fetchall()
        return(data)

    def disp_past_events(self):
        cursor.execute("SELECT * FROM event WHERE date <= NOW()")
        data = cursor.fetchall()
        return(data)

    def disp_event_details(self, id):
        cursor.execute("SELECT * FROM event WHERE event_code = '"+id+"'")
        data = cursor.fetchall()
        return(data)

    def get_upcoming_event_code_list(self):
        cursor.execute("SELECT event_code, title from event WHERE date >= NOW() order by date")
        data = cursor.fetchall()
        return(data)

    def get_event_id(self, name):
        cursor.execute("SELECT event_code FROM event WHERE title = '" + name + "' ")
        data = cursor.fetchall()[0][0]
        return(data)

    def insert_event(self, event_code, title, date, desc, venue, price, image, cord):
        cursor.execute("INSERT INTO event(event_code, title, date, description, venue, price, image, coordinator) VALUES('"+event_code+"','"+title+"','"+date+"','"+desc+"','"+venue+"','"+price+"','"+image+"', '"+cord+"')")
        conn.commit()
        return

    def del_event(self, code):
        cursor.execute("DELETE FROM event WHERE event_code = '"+code+"'")
        data = cursor.fetchall()
        return(data)

    def insert_register(self, event_id, user_id, number):
        cursor.execute("INSERT INTO registrations(event_id,user_id,number) VALUES('"+event_id+"',"+ str(user_id) +", "+str(number)+") ")
        conn.commit()
        print("hello")
        return

    def disp_win_details(self, id):
        cursor.execute("SELECT * FROM attended_winners WHERE event_id = '"+id+"'")
        data = cursor.fetchall()
        return(data)

    def insert_win_details(self, id, user_id, rank):
        cursor.execute("INSERT INTO attended_winners(event_id,user_id,ranking) VALUES('"+id+"',"+ str(user_id) +", "+str(rank)+") ")
        conn.commit()
        return

    def show_win_details(self):
        cursor.execute("SELECT * FROM attended_winners")
        conn.commit()
        return

    def get_cname(self, cid):
        cursor.execute("SELECT name FROM coordinators WHERE cid='"+ str(cid) +"' ")
        data = cursor.fetchall()
        return(data)

    def check_login(self, uname, passw):
        cursor.execute("SELECT password FROM auth_user WHERE username='"+uname+"' ")
        print(cursor.execute("SELECT password FROM auth_user WHERE username='"+uname+"' "))
        data = cursor.fetchall()[0]
        data = data[0]
        if passw == data:
            return True;
