# 🚀 Complete Setup Guide - ClassHub

## Quick Start (5 Minutes)

### 1. Download or Clone the Project

Create a folder structure like this:

```
google_classroom_clone/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── class_view.html
│   ├── create_class.html
│   ├── join_class.html
│   ├── create_assignment.html
│   └── assignment_view.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── database/          (will be auto-created)
└── uploads/
    └── assignments/   (will be auto-created)
```

### 2. Install Python (if not installed)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation
- Verify: Open CMD and type `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

### 3. Create Virtual Environment

```bash
# Navigate to project folder
cd google_classroom_clone

# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

### 6. Open in Browser

Go to: `http://127.0.0.1:5000`

---

## 📖 Detailed Walkthrough

### First Time Setup

#### Create Your First Account

1. Click "Create Account" on the login page
2. Fill in:
   - Full Name: "John Doe"
   - Email: "teacher@example.com"
   - Password: (minimum 6 characters)
   - Role: Select "Teacher"
3. Click "Create Account"
4. You'll be redirected to login

#### Login

1. Enter your email and password
2. Click "Sign In"
3. You'll see your dashboard

### As a Teacher

#### Create Your First Class

1. On dashboard, click "+ Create Class"
2. Fill in:
   - Class Title: "Introduction to Web Development" (required)
   - Section: "CS101 - Fall 2025" (optional)
   - Subject: "Computer Science" (optional)
   - Room: "Room 305" (optional)
3. Click "Create Class"
4. You'll see a class code like "ABC123" - save this!

#### Post an Announcement

1. Click on your class card
2. You'll be on the "Stream" tab
3. Click "+ Post Announcement"
4. Fill in:
   - Title: "Welcome to Class!"
   - Content: "Hello everyone, welcome to the course..."
5. Click "Post"

#### Create an Assignment

1. In your class, click "Classwork" tab
2. Click "+ Create Assignment"
3. Fill in:
   - Title: "HTML Basics"
   - Description: "Create a simple HTML page..."
   - Type: "Assignment"
   - Due Date: Select a date
   - Points: "100"
4. Click "Create Assignment"

### As a Student

#### Create Student Account

1. Logout from teacher account
2. Register with:
   - Full Name: "Jane Student"
   - Email: "student@example.com"
   - Password: (minimum 6 characters)
   - Role: Select "Student"

#### Join a Class

1. On dashboard, click "+ Join Class"
2. Enter the 6-character class code from your teacher (e.g., "ABC123")
3. Click "Join Class"
4. The class will appear on your dashboard

#### Submit an Assignment

1. Click on your class
2. Go to "Classwork" tab
3. Click on an assignment
4. Click "Choose File" to upload your work
5. (Optional) Add a comment
6. Click "Turn In"
7. You'll see a green "✓ Submitted" message

---

## 🔧 Troubleshooting

### Problem: "Module not found" error

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in terminal

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Port 5000 already in use

**Solution:**
```python
# Edit app.py, change the last line to:
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed port
```

### Problem: Database error or corruption

**Solution:**
```bash
# Delete the database file
rm database/classroom.db  # Linux/macOS
del database\classroom.db  # Windows

# Run the app again - it will create a new database
python app.py
```

### Problem: File upload fails

**Solution:**
```bash
# Make sure uploads folder exists
mkdir -p uploads/assignments  # Linux/macOS
mkdir uploads\assignments      # Windows

# Check file size (must be under 16MB)
# Check file extension (PDF, DOC, DOCX, TXT, JPG, PNG, ZIP)
```

### Problem: Can't login after registration

**Solution:**
- Make sure you're using the correct email
- Password is case-sensitive
- Check for typos
- Try registering a new account with different email

### Problem: CSS not loading

**Solution:**
```bash
# Hard refresh in browser
# Windows/Linux: Ctrl + Shift + R
# macOS: Cmd + Shift + R

# Or clear browser cache
```

---

## 🖥️ Development Tips

### Running in Debug Mode

Debug mode is already enabled in `app.py`. This gives you:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Stopping the Server

Press `Ctrl + C` in the terminal

### Viewing Database

You can inspect the database using:

```bash
# Install SQLite browser
pip install sqlite-web

# View database
sqlite_web database/classroom.db
```

Or use a GUI tool like:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [DBeaver](https://dbeaver.io/)

### Checking Logs

Flask logs appear in the terminal where you ran `python app.py`

---

## 🌐 Deployment (Optional)

### Deploy to Production

**⚠️ Important: Before deploying to production:**

1. Change the secret key in `app.py`:
```python
app.secret_key = 'your-secure-random-key-here'  # Generate a strong key
```

2. Disable debug mode:
```python
if __name__ == '__main__':
    app.run(debug=False)
```

3. Use a production database (PostgreSQL instead of SQLite)

4. Set up proper file storage (AWS S3 or similar)

5. Use a production server (Gunicorn + Nginx)

### Quick Deploy to Heroku

```bash
# Install Heroku CLI
# Then:

heroku login
heroku create your-app-name
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

---

## 📚 Using the Application

### Teacher Workflow

1. **Setup** → Create classes
2. **Communicate** → Post announcements
3. **Assign** → Create assignments and quizzes
4. **Monitor** → Check student submissions
5. **Engage** → View class roster

### Student Workflow

1. **Enroll** → Join classes with codes
2. **Stay Updated** → Check stream for announcements
3. **Complete Work** → Submit assignments on time
4. **Track Progress** → View upcoming due dates

---

## 🎯 Testing the Application

### Test Scenario 1: Teacher creates class, student joins

1. Create teacher account
2. Create a class (note the class code)
3. Logout
4. Create student account
5. Join class with code
6. Verify student appears in "People" tab

### Test Scenario 2: Assignment submission

1. As teacher, create an assignment
2. Logout and login as student
3. Go to assignment and submit a file
4. Login as teacher
5. Verify submission (future feature)

### Test Scenario 3: Multiple classes

1. Create 3 different classes
2. Verify they all show on dashboard
3. Each has unique class code
4. Can switch between them

---

## ❓ FAQ

**Q: Can I have multiple teachers for one class?**  
A: Not in the current version. Each class has one teacher.

**Q: Can students see each other's submissions?**  
A: No, submissions are private between student and teacher.

**Q: Is there a maximum number of classes or students?**  
A: No hard limits, but SQLite performance may degrade with many thousands of users.

**Q: Can I reset my password?**  
A: Not in the current version. You'll need to register a new account or manually update the database.

**Q: Where are uploaded files stored?**  
A: In the `uploads/assignments/` folder in your project directory.

**Q: Can I customize the colors?**  
A: Yes! Edit the CSS variables in `static/css/styles.css`:
```css
:root {
    --primary: #2d5f5d;  /* Change this */
    --primary-light: #5a8e8b;  /* And this */
    /* etc... */
}
```

---

## 🎓 Learning Resources

### Learn More About:

- **Flask:** [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **Jinja2 Templates:** [jinja.palletsprojects.com](https://jinja.palletsprojects.com/)
- **SQLite:** [sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- **HTML/CSS:** [developer.mozilla.org](https://developer.mozilla.org/)

---

## 📞 Support

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review the error message in terminal
3. Check browser console (F12) for JavaScript errors
4. Verify all files are in correct locations
5. Try deleting database and starting fresh

---

## ✅ Setup Checklist

- [ ] Python 3.7+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Project structure matches the layout
- [ ] Can run `python app.py` without errors
- [ ] Can access http://127.0.0.1:5000 in browser
- [ ] Can create an account
- [ ] Can login successfully
- [ ] Teacher can create a class
- [ ] Student can join a class
- [ ] Assignments can be created and submitted

Once all items are checked, you're ready to use ClassHub! 🎉