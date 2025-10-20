from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "change_this_secret"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dev@05ar20",
        database="crimedatabase"
    )

# ---------- HOME ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- GENERIC VIEW: list table ----------
def fetch_all(table):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM `{table}`")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.route('/view/<table>')
def view_table(table):
    valid = ['Station','Officer','CaseFile','Crime','Criminal','Victim','Witness','Station_Log','Case_Log','Criminal_Log']
    if table not in valid:
        flash("Invalid table", "danger")
        return redirect(url_for('index'))
    rows = fetch_all(table)
    return render_template('table_view.html', table=table, rows=rows)

# ---------- STATION ----------
@app.route('/station/new', methods=['GET','POST'])
def station_new():
    if request.method == 'POST':
        name = request.form.get('station_name')
        location = request.form.get('location')
        phone = request.form.get('phone')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Station(station_name, location, phone) VALUES (%s,%s,%s)",
                    (name, location, phone))
        conn.commit()
        cur.close(); conn.close()
        flash("Station added", "success")
        return redirect(url_for('view_table', table='Station'))
    return render_template('station_form.html')

# ---------- OFFICER ----------
@app.route('/officer/new', methods=['GET','POST'])
def officer_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT station_id, station_name FROM Station")
    stations = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        name = request.form.get('officer_name')
        rank = request.form.get('officer_rank')
        station_id = request.form.get('station_id') or None
        contact_no = request.form.get('contact_no')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Officer(officer_name, officer_rank, station_id, contact_no) VALUES (%s,%s,%s,%s)",
                    (name, rank, station_id, contact_no))
        conn.commit()
        cur.close(); conn.close()
        flash("Officer added", "success")
        return redirect(url_for('view_table', table='Officer'))
    return render_template('officer_form.html', stations=stations)

# ---------- CASE (normal insert) ----------
@app.route('/case/new', methods=['GET','POST'])
def case_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT officer_id, officer_name FROM Officer")
    officers = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        title = request.form.get('case_title')
        ctype = request.form.get('case_type')
        officer_id = request.form.get('officer_id') or None
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO CaseFile(case_title, case_type, date_reported, status, officer_id) VALUES (%s,%s,CURDATE(),'Open',%s)",
                    (title, ctype, officer_id))
        conn.commit()
        cur.close(); conn.close()
        flash("Case added", "success")
        return redirect(url_for('view_table', table='CaseFile'))
    return render_template('case_form.html', officers=officers)

# ---------- CRIME ----------
@app.route('/crime/new', methods=['GET','POST'])
def crime_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT case_id, case_title FROM CaseFile")
    cases = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        case_id = request.form.get('case_id') or None
        desc = request.form.get('crime_description')
        crime_date = request.form.get('crime_date') or None
        location = request.form.get('crime_location')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Crime(case_id, crime_description, crime_date, crime_location) VALUES (%s,%s,%s,%s)",
                    (case_id, desc, crime_date, location))
        conn.commit()
        cur.close(); conn.close()
        flash("Crime recorded", "success")
        return redirect(url_for('view_table', table='Crime'))
    return render_template('crime_form.html', cases=cases)

# ---------- CRIMINAL ----------
@app.route('/criminal/new', methods=['GET','POST'])
def criminal_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT crime_id, crime_description FROM Crime")
    crimes = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age') or None
        address = request.form.get('address')
        crime_id = request.form.get('crime_id') or None
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Criminal(name, gender, age, address, crime_id) VALUES (%s,%s,%s,%s,%s)",
                    (name, gender, age, address, crime_id))
        conn.commit()
        cur.close(); conn.close()
        flash("Criminal registered", "success")
        return redirect(url_for('view_table', table='Criminal'))
    return render_template('criminal_form.html', crimes=crimes)

# ---------- VICTIM ----------
@app.route('/victim/new', methods=['GET','POST'])
def victim_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT case_id, case_title FROM CaseFile")
    cases = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age') or None
        contact_no = request.form.get('contact_no')
        address = request.form.get('address')
        case_id = request.form.get('case_id') or None
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Victim(name, age, contact_no, address, case_id) VALUES (%s,%s,%s,%s,%s)",
                    (name, age, contact_no, address, case_id))
        conn.commit()
        cur.close(); conn.close()
        flash("Victim added", "success")
        return redirect(url_for('view_table', table='Victim'))
    return render_template('victim_form.html', cases=cases)

# ---------- WITNESS ----------
@app.route('/witness/new', methods=['GET','POST'])
def witness_new():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT case_id, case_title FROM CaseFile")
    cases = cur.fetchall()
    cur.close(); conn.close()
    if request.method == 'POST':
        name = request.form.get('name')
        contact_no = request.form.get('contact_no')
        statement = request.form.get('statement')
        case_id = request.form.get('case_id') or None
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Witness(name, contact_no, statement, case_id) VALUES (%s,%s,%s,%s)",
                    (name, contact_no, statement, case_id))
        conn.commit()
        cur.close(); conn.close()
        flash("Witness recorded", "success")
        return redirect(url_for('view_table', table='Witness'))
    return render_template('witness_form.html', cases=cases)

# ---------- STORED PROCEDURE ENDPOINTS ----------
@app.route('/proc/addcase', methods=['GET','POST'])
def proc_addcase():
    officers = fetch_all('Officer')
    result = None
    if request.method == 'POST':
        title = request.form.get('title')
        ctype = request.form.get('type')
        officer_id = request.form.get('officer_id') or None
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.callproc('AddCaseWithOfficer', [title, ctype, officer_id])
        for r in cur.stored_results():
            result = r.fetchall()
        conn.commit()
        cur.close(); conn.close()
        flash("Stored procedure executed", "success")
    return render_template('proc_addcase.html', officers=officers, result=result)

@app.route('/proc/addvictim', methods=['GET','POST'])
def proc_addvictim():
    cases = fetch_all('CaseFile')
    result = None
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age') or None
        contact_no = request.form.get('contact_no')
        address = request.form.get('address')
        case_id = request.form.get('case_id') or None
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.callproc('AddVictim', [name, age, contact_no, address, case_id])
        for r in cur.stored_results():
            result = r.fetchall()
        conn.commit()
        cur.close(); conn.close()
        flash("Stored procedure executed", "success")
    return render_template('proc_addvictim.html', cases=cases, result=result)

@app.route('/proc/registercriminal', methods=['GET','POST'])
def proc_registercriminal():
    crimes = fetch_all('Crime')
    result = None
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age') or None
        address = request.form.get('address')
        crime_id = request.form.get('crime_id') or None
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.callproc('RegisterCriminal', [name, gender, age, address, crime_id])
        for r in cur.stored_results():
            result = r.fetchall()
        conn.commit()
        cur.close(); conn.close()
        flash("Stored procedure executed", "success")
    return render_template('proc_registercriminal.html', crimes=crimes, result=result)

@app.route('/proc/closecase', methods=['GET','POST'])
def proc_closecase():
    cases = fetch_all('CaseFile')
    result = None
    if request.method == 'POST':
        case_id = request.form.get('case_id')
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.callproc('CloseCase', [case_id])
        for r in cur.stored_results():
            result = r.fetchall()
        conn.commit()
        cur.close(); conn.close()
        flash("Stored procedure executed", "success")
    return render_template('proc_closecase.html', cases=cases, result=result)

# ---------- VIEW LOGS ----------
@app.route('/logs/<logtable>')
def view_logs(logtable):
    valid = ['Station_Log','Case_Log','Criminal_Log']
    if logtable not in valid:
        flash("Invalid log table", "danger")
        return redirect(url_for('index'))
    rows = fetch_all(logtable)
    return render_template('logs_view.html', table=logtable, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
