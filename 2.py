from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
cur = None
try:
    print("ready1")
    connection=mysql.connector.connect(user='root', password='201012', host='localhost', database='proj')
    cur= connection.cursor(buffered=True)
    print("ready2")
except:
    print("not working!")

app = Flask(__name__, template_folder = 'Templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        if 'home' in request.form:
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        username = details['fname']
        password = details['lname']
        if username == "user" and password == "12345":
            cur.execute("INSERT INTO Login(username, password) VALUES ('"+username+"','"+password+"');")
            connection.commit()
            return redirect(url_for('main'))
        elif username != "user" and password == "12345":
            return 'Wrong username!'
        elif password != "12345" and username == "user":
            return 'Wrong password!'
        else:
            return 'Wrong username and password'
    else:
        return render_template('login.html')


@app.route('/main_page', methods=['GET','POST'])
def main():
    if request.method == "POST":
        if 'Flights Info' in request.form:
            return redirect(url_for('flights_info'))
        if 'Routes Info' in request.form:
            return redirect(url_for('routes_info'))
        if 'Runways Info' in request.form:
            return redirect(url_for('runways_info'))
        if 'Add Flight Details' in request.form:
            return redirect(url_for('flight_details'))
        if 'Arrival' in request.form:
            return redirect(url_for('arrival'))
        if 'Landing' in request.form:
            return redirect(url_for('landing'))
        if 'Shifting' in request.form:
            return redirect(url_for('shifting'))
        if 'Leaving' in request.form:
            return redirect(url_for('leaving'))
        if 'Takeoff' in request.form:
            return redirect(url_for('takeoff'))
        if 'Departure' in request.form:
            return redirect(url_for('departure'))
        if 'Add Runway' in request.form:
            return redirect(url_for('add_runway'))
        if 'Add Route' in request.form:
            return redirect(url_for('add_route'))
    else:
        qry = "Select * from Schedule"
        cur.execute(qry)

        res = cur.fetchall()
        return render_template('main.html', res=res)


@app.route('/flights_info', methods=['GET','POST'])
def flights_info():
    qry = "SELECT * from FlightAir"
    cur.execute(qry)
    
    res = cur.fetchall()
    return render_template('flights_info.html', res=res)


@app.route('/routes_info', methods=['GET','POST'])
def routes_info():
    qry = "SELECT * from Route"
    cur.execute(qry)
    
    res = cur.fetchall()
    return render_template('routes_info.html', res=res)


@app.route('/runways_info', methods=['GET','POST'])
def runways_info():
    qry = "SELECT * from Runway"
    cur.execute(qry)
    res = cur.fetchall()
    return render_template('runways_info.html', res=res)


@app.route('/arrival', methods=['GET','POST'])
def arrival():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        landing = details['landing']
        leaving = details['leaving']
        duration = details['duration']
        departure = details['departure']
        cur.execute("INSERT INTO FlightAir(f_no, landing, leaving, duration, arrival, departure) VALUES ('"+f_no+"', '"+landing+"', '"+leaving+"', '"+duration+"', TIME(NOW()), '"+departure+"');")
        connection.commit()
        cur.execute("select min(r_no) from Route where status = 'unoccupied';")
        r = cur.fetchone()
#        print(r[0],"-----") 
        cur.execute("update Route set status = 'occupied' where r_no = '"+str(r[0])+"';")
        connection.commit()
        cur.execute("update FlightAir set r_no = '"+str(r[0])+"' where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("insert into Schedule(Time, f_no, task) VALUES ('"+landing+"', '"+f_no+"', 'landing'), ('"+leaving+"', '"+f_no+"', 'leaving'), (ADDTIME('"+duration+"', '"+landing+"'), '"+f_no+"', 'shifting'), (ADDTIME('"+leaving+"', '"+duration+"'), '"+f_no+"', 'takeoff'), ('"+departure+"', '"+f_no+"', 'departure');")
        connection.commit()
        return redirect(url_for('main'))

    else:
        return render_template('arrival.html')


@app.route('/landing', methods=['GET','POST'])
def landing():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        sql_Query = "select min(run_no) from Runway where status = 'unoccupied';"
        cur = connection.cursor()
        cur.execute(sql_Query)
        record = cur.fetchone()
        if record[0] is not None:
            RunNo = int(record[0])
            cur.execute("update Runway set status = 'occupied' where run_no = '"+str(RunNo)+"';")
            connection.commit()
        else:
            cur.execute("select run_no from Runway where Time = (select min(Time) from Runway);")
            record1 = cur.fetchone()
            RunNo = int(record1[0])
            cur.execute("select f_no from FlightAir where run_no = "+str(RunNo)+";")
            record2 = cur.fetchone()
            f = record2[0]
            cur.execute("update FlightAir set run_no = NULL where f_no = '"+f+"';")
            connection.commit()
        cur.execute("update Route set status = 'unoccupied' where r_no = (select r_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update Runway set Time =  (select landing from FlightAir where f_no = '"+f_no+"') where run_no = "+str(RunNo)+";")
        connection.commit()
        cur.execute("update FlightAir set run_no = '"+str(RunNo)+"' where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("update FlightAir set r_no = NULL where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("delete from Schedule where f_no = '"+f_no+"' and task = 'landing';")
        connection.commit()
        return redirect(url_for('main'))
    else:
        return render_template('landing.html')


@app.route('/shifting', methods=['GET','POST'])
def shifting():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        sql_Query = "select min(p_no) from Hangar where status = 'unoccupied';"
        cur = connection.cursor()
        cur.execute(sql_Query)
        record = cur.fetchone()
        if record[0] is not None:
            PNo = int(record[0])
            cur.execute("update Hangar set status = 'occupied' where p_no = '"+str(PNo)+"';")
            connection.commit()
        else:
            cur.execute("select p_no from Hangar where Time = (select min(Time) from Hangar);")
            record1 = cur.fetchone()
            PNo = int(record1[0])
            cur.execute("select f_no from FlightAir where p_no = "+str(PNo)+";")
            record2 = cur.fetchone()
            f = record2[0]
            cur.execute("update FlightAir set p_no = NULL where f_no = '"+f+"';")
            connection.commit()
        cur.execute("update Runway set status = 'unoccupied' where run_no = (select run_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update Runway set Time = NULL where run_no = (select run_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update Hangar set Time =  (select ADDTIME(landing, duration) from FlightAir where f_no = '"+f_no+"') where p_no = "+str(PNo)+";")
        connection.commit()
        cur.execute("update FlightAir set p_no = '"+str(PNo)+"' where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("update FlightAir set run_no = NULL where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("delete from Schedule where f_no = '"+f_no+"' and task = 'shifting';")
        connection.commit()
        return redirect(url_for('main'))
    else:
        return render_template('shifting.html')


@app.route('/leaving', methods=['POST','GET'])
def leaving():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        sql_Query = "select min(run_no) from Runway where status = 'unoccupied';"
        cur = connection.cursor()
        cur.execute(sql_Query)
        record = cur.fetchone()
        if record[0] is not None:
            RunNo = int(record[0])
            cur.execute("update Runway set status = 'occupied' where run_no = '"+str(RunNo)+"';")
            connection.commit()
        else:
            cur.execute("select run_no from Runway where Time = (select min(Time) from Runway);")
            record1 = cur.fetchone()
            RunNo = int(record1[0])
            cur.execute("select f_no from FlightAir where run_no = "+str(RunNo)+";")
            record2 = cur.fetchone()
            f = record2[0]
            cur.execute("update FlightAir set run_no = NULL where f_no = '"+f+"';")
            connection.commit()
        cur.execute("update Hangar set status = 'unoccupied' where p_no = (select p_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update Hangar set Time = NULL where p_no = (select p_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update Runway set Time =  (select leaving from FlightAir where f_no = '"+f_no+"') where run_no = "+str(RunNo)+";")
        connection.commit()
        cur.execute("update FlightAir set run_no = '"+str(RunNo)+"' where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("update FlightAir set p_no = NULL where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("delete from Schedule where f_no = '"+f_no+"' and task = 'leaving';")
        connection.commit()
        return redirect(url_for('main'))
    else:
        return render_template('leaving.html')


@app.route('/takeoff', methods=['POST','GET'])
def takeoff():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        sql_Query = "select min(r_no) from Route where status = 'unoccupied';"
        cur = connection.cursor()
        cur.execute(sql_Query)
        record = cur.fetchone()
        if record[0] is not None:
            RNo = int(record[0])
            cur.execute("update Route set status = 'occupied' where r_no = '"+str(RNo)+"';")
            connection.commit()
        else:
            cur.execute("select r_no from Route where Time = (select min(Time) from Route);")
            record1 = cur.fetchone()
            RNo = int(record1[0])
            cur.execute("select f_no from FlightAir where r_no = "+str(RNo)+";")
            record2 = cur.fetchone()
            f = record2[0]
            cur.execute("update FlightAir set r_no = NULL where f_no = '"+f+"';")
            connection.commit()
        cur.execute("update Runway set status = 'unoccupied' where run_no = (select run_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("update FlightAir set r_no = '"+str(RNo)+"' where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("update FlightAir set run_no = NULL where f_no = '"+f_no+"';")
        connection.commit()
        cur.execute("delete from Schedule where f_no = '"+f_no+"' and task = 'takeoff';")
        connection.commit()
        return redirect(url_for('main'))
    else:
        return render_template('takeoff.html')


@app.route('/departure', methods=['POST','GET'])
def departure():
    if request.method == "POST":
        details = request.form
        f_no = details['f_no']
        cur = connection.cursor()
        cur.execute("update Route set status = 'unoccupied' where r_no = (select r_no from FlightAir where f_no = '"+f_no+"');")
        connection.commit()
        cur.execute("delete from Schedule where f_no = '"+f_no+"' and task = 'departure';")
        connection.commit()
        cur.execute("delete from FlightAir where f_no = '"+f_no+"';")
        return redirect(url_for('main'))
    else:
        return render_template('departure.html')


@app.route('/add_route', methods=['GET','POST'])
def add_route():
    if request.method == "POST":
        details = request.form
        r_no = details['r_no']
        cur.execute("INSERT INTO Route(r_no, status) VALUES ('"+r_no+"', 'unoccupied');")
        return redirect(url_for('main'))
    else:
        return render_template('add_route.html')

@app.route('/add_runway', methods=['GET','POST'])
def add_runway():
    if request.method == "POST":
        details = request.form
        run_no = details['run_no']
        cur.execute("INSERT INTO Runway(run_no, status) VALUES ('"+run_no+"', 'unoccupied');")
        return redirect(url_for('main'))
    else:
        return render_template('add_runway.html')


if __name__ == '__main__':
    app.run(debug = True)