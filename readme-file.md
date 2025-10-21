# ClassHub - Google Classroom Clone

A full-featured Google Classroom-style learning management system built with Flask, HTML, CSS, and JavaScript.

![ClassHub](https://via.placeholder.com/800x400/2d5f5d/ffffff?text=ClassHub)

## 🌟 Features

### User Management
- **Role-based authentication** (Teacher/Student)
- Secure password hashing with Werkzeug
- Session-based login system
- User profile management

### Classes
- **Teachers can:**
  - Create unlimited classes
  - Generate unique class codes
  - Manage class details (title, section, subject, room)
  - Post announcements
  - Create assignments, quizzes, and materials
  - View student submissions

- **Students can:**
  - Join classes using class codes
  - View announcements
  - Submit assignments with file uploads
  - Track due dates and grades

### Interface
- **Modern, responsive design** with green color theme
- Mobile-first approach
- Tabbed navigation (Stream, Classwork, People)
- Real-time flash messages
- Smooth animations and transitions
- Accessible UI with keyboard navigation

### Technical Features
- SQLite database for data persistence
- File upload handling (up to 16MB)
- AJAX-powered announcements
- Dynamic content loading
- Search functionality
- Copy-to-clipboard for class codes

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd google_classroom_clone

# Or download and extract the ZIP file
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### Step 5: Access the Application

1. Open your web browser
2. Navigate to `http://127.0.0.1:5000/`
3. Create an account (choose Teacher or Student role)
4. Start creating or joining classes!

## 📁 Project Structure

```
google_classroom_clone/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── database/
│   └── classroom.db           # SQLite database (auto-created)
│
├── templates/
│   ├── base.html              # Base template with navbar
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── class_view.html        # Individual class page
│   ├── create_class.html      # Create class form
│   ├── join_class.html        # Join class form
│   ├── create_assignment.html # Create assignment form
│   └── assignment_view.html   # Assignment details & submission
│
├── static/
│   ├── css/
│   │   └── styles.css         # All styles with green theme
│   └── js/
│       └── main.js            # Client-side JavaScript
│
└── uploads/
    └── assignments/           # Student submission files
```

## 🎨 Design Theme

The application uses a professional green color palette:
- Primary: `#2d5f5d` (Deep teal)
- Primary Light: `#5a8e8b` (Medium teal)
- Accent: `#b8d4ce` (Light mint)
- Background: `#f5f7f6` (Soft gray-green)

## 💡 Usage Guide

### For Teachers

1. **Create a Class:**
   - Click "Create Class" on dashboard
   - Fill in class details
   - Get a unique class code to share with students

2. **Post Announcements:**
   - Go to class → Stream tab
   - Click "Post Announcement"
   - Add title and content

3. **Create Assignments:**
   - Go to class → Classwork tab
   - Click "Create Assignment"
   - Fill in details, set due date and points

### For Students

1. **Join a Class:**
   - Click "Join Class" on dashboard
   - Enter the 6-character class code from your teacher

2. **Submit Assignments:**
   - Go to class → Classwork tab
   - Click on assignment
   - Upload file and/or add comment
   - Click "Turn In"

## 🔒 Security Features

- Password hashing using Werkzeug's `generate_password_hash`
- Session-based authentication
- Protected routes with decorators
- Role-based access control
- Secure file upload with extension validation
- SQL injection protection with parameterized queries

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Web framework
- **Werkzeug 3.0.1** - WSGI utilities and security
- **SQLite3** - Database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox/Grid
- **JavaScript (ES6)** - Client-side interactivity
- **Google Fonts (Inter)** - Typography

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home (redirects to login/dashboard) |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/dashboard` | GET | User dashboard |
| `/create-class` | GET, POST | Create new class (teacher) |
| `/join-class` | GET, POST | Join class (student) |
| `/class/<id>` | GET | View class details |
| `/class/<id>/post-announcement` | POST | Post announcement (AJAX) |
| `/class/<id>/create-assignment` | GET, POST | Create assignment (teacher) |
| `/assignment/<id>` | GET, POST | View/submit assignment |

## 🐛 Known Limitations

1. **No real-time updates** - Users must refresh to see new content
2. **Basic comment system** - Comments are displayed but not fully interactive
3. **No grade management** - Teachers can't assign grades yet
4. **Limited file types** - Only specific formats allowed
5. **No email notifications** - Users don't receive email alerts
6. **No calendar integration** - Due dates aren't synced to a calendar
7. **Single teacher per class** - No co-teacher functionality
8. **No class archiving** - Can't archive old classes

## 🔮 Future Enhancements

- Real-time notifications using WebSockets
- Grade book and grading rubrics
- Calendar integration
- Email notifications
- File preview without download
- Rich text editor for announcements
- Mobile app
- Video conferencing integration
- Discussion forums
- Parent/Guardian accounts

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your own learning purposes.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a Google Classroom clone demonstration