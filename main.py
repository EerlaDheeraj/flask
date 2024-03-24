# from flask import Flask, render_template, request, redirect, url_for, session
# import mysql.connector
# import bcrypt

# # MySQL connection
# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Dheeraj14",
#   database="resume_db"
# )
# cursor = db.cursor()

# app = Flask(__name__)
# app.secret_key = "b'Q\xc4\xf6\xb2{\xa2n\xa3\xec\xb8\n\x05\xd5\r!=\xdf\x7f\xf1\x0f\x17\x95\xdf.'"

# # Helper functions
# def hash_password(password):
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode(), salt)
#     return hashed.decode()

# def verify_password(password, hashed):
#     return bcrypt.checkpw(password.encode(), hashed.encode())

# # Route for the home page
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         job_id = request.form["job_id"]
#         resume_file = request.files["resume_file"]
#         resume_data = resume_file.read()
#         try:
#             cursor.execute("INSERT INTO resumes (job_id, name, resume_data) VALUES (%s, %s, %s)", (job_id, resume_file.filename, resume_data))
#             db.commit()
#             return "Resume uploaded successfully"
#         except mysql.connector.Error as err:
#             return f"Error: {err}"

#     cursor.execute("SELECT id, title, description FROM job_postings")
#     job_postings = cursor.fetchall()
#     return render_template("home.html", job_postings=job_postings)

# # Route for the admin login page
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         if verify_credentials(username, password):
#             session["logged_in"] = True
#             session["admin_id"] = get_admin_id(username)
#             return redirect(url_for("admin_dashboard"))
#         else:
#             return "Invalid username or password"

#     return render_template("login.html")

# # Route for the admin signup page
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         confirm_password = request.form["confirm_password"]
#         if password != confirm_password:
#             return "Passwords do not match"
#         else:
#             hashed_password = hash_password(password)
#             try:
#                 cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, hashed_password))
#                 db.commit()
#                 return "Account created successfully"
#             except mysql.connector.Error as err:
#                 return f"Error: {err}"

#     return render_template("signup.html")

# # Route for the admin dashboard
# @app.route("/admin_dashboard", methods=["GET", "POST"])
# def admin_dashboard():
#     if "logged_in" not in session or not session["logged_in"]:
#         return redirect(url_for("login"))

#     if request.method == "POST":
#         job_title = request.form["job_title"]
#         job_description = request.form["job_description"]
#         try:
#             cursor.execute("INSERT INTO job_postings (title, description) VALUES (%s, %s)", (job_title, job_description))
#             db.commit()
#             return "Job posting added successfully"
#         except mysql.connector.Error as err:
#             return f"Error: {err}"

#     cursor.execute("SELECT job_postings.title, resumes.name, resumes.resume_data FROM resumes JOIN job_postings ON resumes.job_id = job_postings.id")
#     applications = cursor.fetchall()
#     return render_template("admin_dashboard.html", applications=applications)

# # Route for logging out
# @app.route("/logout")
# def logout():
#     session.pop("logged_in", None)
#     session.pop("admin_id", None)
#     return redirect(url_for("login"))

# def verify_credentials(username, password):
#     cursor.execute("SELECT password FROM admins WHERE username = %s", (username,))
#     result = cursor.fetchone()
#     if result:
#         hashed_password = result[0]
#         return verify_password(password, hashed_password)
#     else:
#         return False

# def get_admin_id(username):
#     cursor.execute("SELECT id FROM admins WHERE username = %s", (username,))
#     result = cursor.fetchone()
#     if result:
#         return result[0]
#     else:
#         return None

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, flash, session
import pymysql
import os

app=Flask(__name__)

app.secret_key=os.urandom(24)

connection = pymysql.connect(host='localhost',user='root',password='Dheeraj14',db='Resume_DB')
cursor = connection.cursor()

@app.route('/')
def default():
    return render_template('user-page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'admin_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `admin_login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    admin_login=cursor.fetchall()
    if len(admin_login)>0:
        session['admin_id']=admin_login[0][2]
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/add_admin', methods=['POST'])
def add_admin():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        flash("Passwords do not match. Please try again.")
    else:
        cursor.execute("""INSERT INTO `admin_login` (`email`,`password`) VALUES ('{}','{}')""".format(email, password) )
        connection.commit()
        return redirect('/login')

@app.route('/add-job-postings')
def add_job_postings():
    return render_template('add-job-postings.html')

@app.route('/logout')
def logout():
    session.pop('admin_id')
    return redirect('/logout')

if __name__=="__main__":
    app.run(debug=True)