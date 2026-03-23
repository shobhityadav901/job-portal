from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "careerhub_123_key" # Sessions ke liye zaroori hai

# Database initialization
def init_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    # Jobs Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT, company TEXT, description TEXT)''')
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# @app.route('/')
# def index():
#     conn = sqlite3.connect('jobs.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
#     jobs = cursor.fetchall()
#     conn.close()
#     return render_template('index.html', jobs=jobs)

@app.route('/')
def index():
    search_query = request.args.get('search') # URL se search term lega
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    if search_query:
        # SQL query jo Title ya Company mein search karegi
        query = "SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ? ORDER BY id DESC"
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
        
    jobs = cursor.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        try:
            conn = sqlite3.connect('jobs.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            conn.close()
            flash("Account created! Ab login karein.")
            return redirect('/login')
        except:
            flash("Username pehle se maujood hai!")
    return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = request.form['username']
#         pwd = request.form['password']
        
#         conn = sqlite3.connect('jobs.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
#         found_user = cursor.fetchone()
#         conn.close()
        
#         if found_user:
#             session['user'] = user
#             return redirect('/')
#         else:
#             flash("Galat Username ya Password!")
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        
        print(f"DEBUG: Login attempt for user: {user}") # Terminal mein dikhega

        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        # Password aur Username dono match hone chahiye
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
        found_user = cursor.fetchone()
        conn.close()
        
        if found_user:
            print("DEBUG: User found! Setting session.")
            session['user'] = user
            return redirect('/')
        else:
            print("DEBUG: User NOT found or wrong password.")
            flash("Invalid Username or Password!")
            return redirect('/login')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/post', methods=['GET', 'POST'])
def post_job():
    if 'user' not in session:
        flash("Job post karne ke liye login karein!")
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        desc = request.form['desc']
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (title, company, description) VALUES (?, ?, ?)", (title, company, desc))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('post_job.html')

@app.route('/delete/<int:id>')
def delete_job(id):
    if 'user' not in session: return redirect('/login')
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')
@app.route('/apply')
def apply():
    # Agar aap chahte hain ki sirf logged-in user hi apply karein:
    if 'user' not in session:
        flash("Apply karne ke liye pehle Login karein!")
        return redirect('/login')
    return render_template('apply.html')

@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Yahan hum bas ek message dikhayenge (Demo ke liye)
    flash("Aapka application successfully submit ho gaya hai!")
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)