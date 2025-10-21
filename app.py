from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads/assignments'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('database/classroom.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Classes table
    c.execute('''CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        section TEXT,
        subject TEXT,
        room TEXT,
        class_code TEXT UNIQUE NOT NULL,
        teacher_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users(id)
    )''')
    
    # Enrollments table
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (student_id) REFERENCES users(id),
        UNIQUE(class_id, student_id)
    )''')
    
    # Announcements table
    c.execute('''CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Assignments table
    c.execute('''CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        points INTEGER,
        assignment_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )''')
    
    # Submissions table
    c.execute('''CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        file_path TEXT,
        comment TEXT,
        status TEXT DEFAULT 'turned_in',
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (assignment_id) REFERENCES assignments(id),
        FOREIGN KEY (student_id) REFERENCES users(id),
        UNIQUE(assignment_id, student_id)
    )''')
    
    # Comments table
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        announcement_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (announcement_id) REFERENCES announcements(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

# Initialize database
os.makedirs('database', exist_ok=True)
init_db()

# Helper functions
def get_db():
    conn = sqlite3.connect('database/classroom.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'teacher':
            flash('Access denied. Teachers only.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def generate_class_code():
    return secrets.token_urlsafe(6)[:6].upper()

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        
        if not all([email, password, full_name, role]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if role not in ['teacher', 'student']:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db()
            conn.execute('INSERT INTO users (email, password, full_name, role) VALUES (?, ?, ?, ?)',
                        (email, hashed_password, full_name, role))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    
    if session['role'] == 'teacher':
        classes = conn.execute('''
            SELECT * FROM classes WHERE teacher_id = ? ORDER BY created_at DESC
        ''', (session['user_id'],)).fetchall()
    else:
        classes = conn.execute('''
            SELECT c.* FROM classes c
            JOIN enrollments e ON c.id = e.class_id
            WHERE e.student_id = ?
            ORDER BY e.enrolled_at DESC
        ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('dashboard.html', classes=classes)

@app.route('/create-class', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_class():
    if request.method == 'POST':
        title = request.form.get('title')
        section = request.form.get('section')
        subject = request.form.get('subject')
        room = request.form.get('room')
        
        if not title:
            flash('Class title is required.', 'danger')
            return redirect(url_for('create_class'))
        
        class_code = generate_class_code()
        
        conn = get_db()
        conn.execute('''
            INSERT INTO classes (title, section, subject, room, class_code, teacher_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, section, subject, room, class_code, session['user_id']))
        conn.commit()
        conn.close()
        
        flash(f'Class created successfully! Class code: {class_code}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_class.html')

@app.route('/join-class', methods=['GET', 'POST'])
@login_required
def join_class():
    if session['role'] != 'student':
        flash('Only students can join classes.', 'warning')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        class_code = request.form.get('class_code').upper()
        
        conn = get_db()
        class_info = conn.execute('SELECT * FROM classes WHERE class_code = ?', (class_code,)).fetchone()
        
        if not class_info:
            flash('Invalid class code.', 'danger')
            conn.close()
            return redirect(url_for('join_class'))
        
        try:
            conn.execute('INSERT INTO enrollments (class_id, student_id) VALUES (?, ?)',
                        (class_info['id'], session['user_id']))
            conn.commit()
            flash(f'Successfully joined {class_info["title"]}!', 'success')
        except sqlite3.IntegrityError:
            flash('You are already enrolled in this class.', 'warning')
        
        conn.close()
        return redirect(url_for('dashboard'))
    
    return render_template('join_class.html')

@app.route('/class/<int:class_id>')
@login_required
def class_view(class_id):
    conn = get_db()
    
    # Get class info
    class_info = conn.execute('SELECT c.*, u.full_name as teacher_name FROM classes c JOIN users u ON c.teacher_id = u.id WHERE c.id = ?', (class_id,)).fetchone()
    
    if not class_info:
        flash('Class not found.', 'danger')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # Check enrollment
    if session['role'] == 'student':
        enrolled = conn.execute('SELECT * FROM enrollments WHERE class_id = ? AND student_id = ?',
                               (class_id, session['user_id'])).fetchone()
        if not enrolled:
            flash('You are not enrolled in this class.', 'danger')
            conn.close()
            return redirect(url_for('dashboard'))
    elif session['role'] == 'teacher' and class_info['teacher_id'] != session['user_id']:
        flash('You do not have access to this class.', 'danger')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # Get announcements
    announcements = conn.execute('''
        SELECT a.*, u.full_name FROM announcements a
        JOIN users u ON a.user_id = u.id
        WHERE a.class_id = ?
        ORDER BY a.created_at DESC
    ''', (class_id,)).fetchall()
    
    # Get assignments
    assignments = conn.execute('''
        SELECT * FROM assignments WHERE class_id = ? ORDER BY due_date
    ''', (class_id,)).fetchall()
    
    # Get people
    teacher = conn.execute('SELECT * FROM users WHERE id = ?', (class_info['teacher_id'],)).fetchone()
    students = conn.execute('''
        SELECT u.* FROM users u
        JOIN enrollments e ON u.id = e.student_id
        WHERE e.class_id = ?
        ORDER BY u.full_name
    ''', (class_id,)).fetchall()
    
    conn.close()
    
    return render_template('class_view.html', 
                          class_info=class_info, 
                          announcements=announcements,
                          assignments=assignments,
                          teacher=teacher,
                          students=students)

@app.route('/class/<int:class_id>/post-announcement', methods=['POST'])
@login_required
def post_announcement(class_id):
    title = request.form.get('title')
    content = request.form.get('content')
    
    if not title or not content:
        return jsonify({'success': False, 'message': 'Title and content are required'}), 400
    
    conn = get_db()
    conn.execute('''
        INSERT INTO announcements (class_id, user_id, title, content)
        VALUES (?, ?, ?, ?)
    ''', (class_id, session['user_id'], title, content))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Announcement posted successfully'})

@app.route('/class/<int:class_id>/create-assignment', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_assignment(class_id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        points = request.form.get('points')
        assignment_type = request.form.get('assignment_type')
        
        if not title:
            flash('Assignment title is required.', 'danger')
            return redirect(url_for('create_assignment', class_id=class_id))
        
        conn = get_db()
        conn.execute('''
            INSERT INTO assignments (class_id, title, description, due_date, points, assignment_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (class_id, title, description, due_date, points, assignment_type))
        conn.commit()
        conn.close()
        
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('class_view', class_id=class_id))
    
    conn = get_db()
    class_info = conn.execute('SELECT * FROM classes WHERE id = ?', (class_id,)).fetchone()
    conn.close()
    
    return render_template('create_assignment.html', class_info=class_info)

@app.route('/assignment/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def assignment_view(assignment_id):
    conn = get_db()
    assignment = conn.execute('SELECT * FROM assignments WHERE id = ?', (assignment_id,)).fetchone()
    
    if not assignment:
        flash('Assignment not found.', 'danger')
        conn.close()
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST' and session['role'] == 'student':
        comment = request.form.get('comment')
        file = request.files.get('file')
        
        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session['user_id']}_{assignment_id}_{filename}")
            file.save(file_path)
        
        try:
            conn.execute('''
                INSERT INTO submissions (assignment_id, student_id, file_path, comment)
                VALUES (?, ?, ?, ?)
            ''', (assignment_id, session['user_id'], file_path, comment))
            conn.commit()
            flash('Assignment submitted successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('You have already submitted this assignment.', 'warning')
        
        conn.close()
        return redirect(url_for('assignment_view', assignment_id=assignment_id))
    
    # Get submission if exists
    submission = None
    if session['role'] == 'student':
        submission = conn.execute('''
            SELECT * FROM submissions WHERE assignment_id = ? AND student_id = ?
        ''', (assignment_id, session['user_id'])).fetchone()
    
    conn.close()
    return render_template('assignment_view.html', assignment=assignment, submission=submission)

@app.route('/uploads/<path:filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)