# 📋 ClassHub Quick Reference

## 🔐 Authentication

| Action | Endpoint | Method |
|--------|----------|--------|
| Register | `/register` | GET, POST |
| Login | `/login` | GET, POST |
| Logout | `/logout` | GET |

**Default Test Accounts** (create these for testing):
```
Teacher:
  Email: teacher@test.com
  Password: teacher123
  
Student:
  Email: student@test.com
  Password: student123
```

---

## 🎯 Quick Commands

### Start Application
```bash
python app.py
```

### Access Application
```
http://127.0.0.1:5000
```

### Stop Application
```
Ctrl + C (in terminal)
```

### Reset Database
```bash
# Backup first (optional)
cp database/classroom.db database/classroom_backup.db

# Delete current database
rm database/classroom.db  # macOS/Linux
del database\classroom.db  # Windows

# Restart app to create fresh database
python app.py
```

---

## 👨‍🏫 Teacher Actions

### Create a Class
1. Dashboard → "+ Create Class"
2. Fill required fields
3. Note the generated class code
4. Share code with students

### Post Announcement
1. Class → Stream tab
2. "+ Post Announcement"
3. Fill title and content
4. Click "Post"

### Create Assignment
1. Class → Classwork tab
2. "+ Create Assignment"
3. Fill details (title required)
4. Set type, due date, points
5. Click "Create Assignment"

### View Student List
1. Class → People tab
2. See teacher + all enrolled students

### Copy Class Code
1. Class page → Hero section
2. Click "Copy" button next to class code
3. Share with students

---

## 👨‍🎓 Student Actions

### Join a Class
1. Dashboard → "+ Join Class"
2. Enter 6-character code
3. Click "Join Class"
4. Class appears on dashboard

### View Announcements
1. Class → Stream tab
2. Scroll through announcements
3. Read updates from teacher

### Submit Assignment
1. Class → Classwork tab
2. Click on assignment
3. Upload file (optional)
4. Add comment (optional)
5. Click "Turn In"

### Check Submission Status
1. Assignment page
2. Green box shows "✓ Submitted" if turned in
3. Shows submission details

---

## 🎨 Customization

### Change Colors

Edit `static/css/styles.css`:

```css
:root {
    --primary: #2d5f5d;        /* Main color */
    --primary-light: #5a8e8b;  /* Lighter shade */
    --primary-dark: #1e3f3d;   /* Darker shade */
    --accent-1: #b8d4ce;       /* Light accent */
    --accent-2: #4a7c78;       /* Dark accent */
}
```

### Change App Name

Edit `templates/base.html`:
```html
<span>ClassHub</span>  <!-- Change to your name -->
```

### Change Logo

Edit `templates/base.html`:
```html
<div class="logo-icon">CH</div>  <!-- Change initials -->
```

---

## 📊 Database Schema

### Tables

**users**
- id, email, password, full_name, role, created_at

**classes**
- id, title, section, subject, room, class_code, teacher_id, created_at

**enrollments**
- id, class_id, student_id, enrolled_at

**announcements**
- id, class_id, user_id, title, content, created_at

**assignments**
- id, class_id, title, description, due_date, points, assignment_type, created_at

**submissions**
- id, assignment_id, student_id, file_path, comment, status, submitted_at

---

## 🔍 Common Issues & Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Can't login | Check email/password spelling |
| Port already in use | Change port in app.py to 5001 |
| Module not found | `pip install -r requirements.txt` |
| Database error | Delete database file and restart |
| CSS not loading | Hard refresh (Ctrl+Shift+R) |
| File won't upload | Check size (<16MB) and format |
| Class code invalid | Check for spaces/typos, use uppercase |

---

## 🎯 Feature Status

### ✅ Implemented
- User registration & login
- Role-based access (teacher/student)
- Create & join classes
- Post announcements
- Create assignments
- Submit assignments with files
- View class roster
- Responsive design
- Flash messages
- Search functionality

### ⏳ Not Yet Implemented
- Grades/grading
- Comments on announcements
- Edit/delete posts
- Email notifications
- Calendar view
- Due date reminders
- File preview
- Rich text editor
- Profile pictures
- Class archives

---

## 📱 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Esc | Close modal |
| Tab | Navigate form fields |
| Enter | Submit forms |

---

## 🌐 Browser Compatibility

✅ **Fully Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

⚠️ **Limited Support:**
- Internet Explorer (not recommended)

---

## 📁 File Upload Limits

| Attribute | Limit |
|-----------|-------|
| Max file size | 16 MB |
| Allowed types | PDF, DOC, DOCX, TXT, JPG, JPEG, PNG, ZIP |
| Multiple files | No (one per submission) |

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Session management
- ✅ Role-based access control
- ✅ SQL injection protection
- ✅ Secure file uploads
- ✅ CSRF protection (Flask)

---

## 📞 Quick Help Commands

### View Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
```

### Update Package
```bash
pip install --upgrade package-name
```

### Create Requirements File
```bash
pip freeze > requirements.txt
```

---

## 💡 Pro Tips

1. **Use descriptive class names** - Makes it easier for students to find
2. **Set due dates** - Helps students prioritize work
3. **Post regular announcements** - Keeps students engaged
4. **Use clear assignment titles** - Students know what to do
5. **Test as both roles** - Create teacher AND student accounts
6. **Copy class codes immediately** - Save them somewhere safe
7. **Backup database regularly** - Copy classroom.db to safe location
8. **Use consistent naming** - Makes searching easier
9. **Check submissions regularly** - Stay on top of student work
10. **Organize with sections** - Use section field for organization

---

## 🚀 Performance Tips

- Clear browser cache regularly
- Use modern browsers
- Avoid uploading huge files (keep under 10MB)
- Don't create thousands of classes (SQLite limits)
- Restart Flask app periodically in development

---

## 📈 Usage Limits (SQLite)

| Resource | Practical Limit |
|----------|----------------|
| Users | ~10,000 |
| Classes | ~1,000 |
| Assignments | ~10,000 |
| File uploads | Limited by disk space |

For larger deployments, consider PostgreSQL.

---

## ✨ Easter Eggs & Hidden Features

1. **Click class code** → Auto-copies to clipboard
2. **Flash messages** → Auto-dismiss after 5 seconds
3. **Tab switching** → No page reload
4. **Responsive search** → Real-time filtering
5. **Gradient headers** → Different colors per class

---

## 📚 Folder Structure Quick Reference

```
Root/
├── app.py              ← Flask application
├── requirements.txt    ← Python packages
├── README.md          ← Full documentation
├── database/
│   └── classroom.db   ← SQLite database
├── templates/         ← HTML files (8 files)
├── static/
│   ├── css/
│   │   └── styles.css ← All styles
│   └── js/
│       └── main.js    ← JavaScript
└── uploads/
    └── assignments/   ← Student files
```

---

## 🎓 Learning Path

1. **Week 1:** Setup & basic usage
2. **Week 2:** Create classes & assignments
3. **Week 3:** Test as student role
4. **Week 4:** Customize colors & branding
5. **Week 5:** Deploy to production (optional)

---

This quick reference covers the most common tasks and issues. For detailed information, see the full README.md and SETUP_GUIDE.md files.