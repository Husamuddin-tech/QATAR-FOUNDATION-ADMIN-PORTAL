# CertifyMe Admin Portal - Backend

A secure Flask-based backend for the Qatar Foundation Admin Portal, providing comprehensive user authentication, opportunity management, and RESTful API endpoints.

### Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+ |
| Framework | Flask 2.3.2 |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Session Management | Flask-Login |
| CORS Support | Flask-CORS |

---

## 📋 Prerequisites

- Python 3.8 or higher installed
- Git (already done if you cloned the repo)
- VS Code or any text editor

---

## ⚙️ Installation & Setup

### Step 1: Clone and Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/Neerajvs32/Test1.git
cd CertifyMe

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

---

## 🏗️ Project Structure

```
CertifyMe/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── models.py                 # Database models (Admin, Opportunity)
├── routes.py                 # API endpoints
├── requirements.txt          # Python dependencies
├── certifyme.db             # SQLite database (auto-created)
│
├── sky/                      # Frontend assets (DO NOT MODIFY)
│   ├── admin.html           # Main HTML file
│   ├── admin.css            # Styling
│   └── admin.js             # Frontend logic (updated with API calls)
│
└── test_api.py              # API testing script
```

---

## 🔐 Features & User Stories

### Phase 1: Authentication (Day 1)

#### US-1.1 - Admin Sign Up
- Create an account with email and password
- Passwords must be at least 8 characters
- Duplicate emails are prevented
- Passwords are securely hashed using scrypt

**Endpoint**: `POST /api/auth/signup`

```json
{
  "name": "John Admin",
  "email": "admin@example.com",
  "password": "securepass123",
  "confirmPassword": "securepass123"
}
```

#### US-1.2 - Admin Login
- Secure login with email and password
- "Remember Me" functionality for extended sessions
- Generic error messages to prevent email enumeration attacks

**Endpoint**: `POST /api/auth/login`

```json
{
  "email": "admin@example.com",
  "password": "securepass123",
  "rememberMe": false
}
```

#### US-1.3 - Forgot Password
- Request password reset link
- Links expire after 1 hour
- Reset links are printed to console (in development)
- Returns success message regardless of email existence (security)

**Endpoint**: `POST /api/auth/forgot`

```json
{
  "email": "admin@example.com"
}
```

#### US-1.4 - Logout
- Secure logout that clears session

**Endpoint**: `POST /api/auth/logout`

---

### Phase 2: Opportunity Management (Day 2)

#### US-2.1 - View All Opportunities
- Retrieve all opportunities created by the logged-in user
- Returns JSON data without page refresh

**Endpoint**: `GET /api/opportunities`

**Response**:
```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": 1,
      "title": "Python Developer Internship",
      "duration": "3 months",
      "start_date": "2026-06-01",
      "description": "Develop web applications",
      "skills": ["Python", "Flask", "SQL"],
      "category": "Technology",
      "future_opportunities": "Full-time position opportunity",
      "max_applicants": 50,
      "created_at": "2026-05-01T14:58:18.186746"
    }
  ]
}
```

#### US-2.2 - Create Opportunity
- Add a new opportunity with all required fields
- Validates category against allowed list
- Skills are stored as JSON array
- Associates opportunity with current logged-in admin

**Endpoint**: `POST /api/opportunities`

```json
{
  "name": "Python Developer Internship",
  "duration": "3 months",
  "startDate": "2026-06-01",
  "description": "Develop web applications using Flask",
  "skills": ["Python", "Flask", "SQL", "REST APIs"],
  "category": "Technology",
  "futureOpportunities": "Full-time position opportunity",
  "maxApplicants": "50"
}
```

**Allowed Categories**: Technology, Business, Design, Marketing, Healthcare, Education

#### US-2.3 - View Opportunity Details
- Retrieve complete details of a specific opportunity
- Only accessible by the creator (admin)

**Endpoint**: `GET /api/opportunities/<id>`

#### US-2.4 - Update Opportunity
- Edit any field of an existing opportunity
- Verifies ownership (admin can only update own opportunities)
- Returns updated opportunity as JSON

**Endpoint**: `PUT /api/opportunities/<id>/edit` or `POST /api/opportunities/<id>/edit`

```json
{
  "name": "Updated Title",
  "duration": "4 months",
  "startDate": "2026-07-01"
}
```

#### US-2.5 - Delete Opportunity
- Remove an opportunity from the database
- Only creator can delete

**Endpoint**: `DELETE /api/opportunities/<id>`

---

## 🧪 Testing the API

### Using the Test Script

```bash
python test_api.py
```

This script tests all endpoints:
- Health check
- Sign up (including duplicate email prevention)
- Login (with session management)
- Create opportunity
- Retrieve opportunities
- Forgot password
- Logout
- Access control (unauthenticated access prevention)

### Using Postman

1. **Sign Up**
   - Method: POST
   - URL: `http://localhost:5000/api/auth/signup`
   - Body (JSON):
   ```json
   {
     "name": "Your Name",
     "email": "your@email.com",
     "password": "password123",
     "confirmPassword": "password123"
   }
   ```

2. **Login**
   - Method: POST
   - URL: `http://localhost:5000/api/auth/login`
   - Body (JSON):
   ```json
   {
     "email": "your@email.com",
     "password": "password123",
     "rememberMe": false
   }
   ```

3. **Create Opportunity**
   - Method: POST
   - URL: `http://localhost:5000/api/opportunities`
   - Headers: Add cookie from login response
   - Body (JSON): See US-2.2 above

---

## 🎨 Frontend Integration

The frontend (`admin.js`) has been fully updated to communicate with the backend API:

### Key Updates:
- ✅ Login form now calls `/api/auth/login`
- ✅ Signup form now calls `/api/auth/signup`
- ✅ Forgot password calls `/api/auth/forgot`
- ✅ Logout calls `/api/auth/logout`
- ✅ Opportunity creation calls `/api/opportunities` (POST)
- ✅ Opportunities are loaded from backend on dashboard view
- ✅ CORS enabled for cross-origin requests
- ✅ Session management with credentials included

### Database Models

#### Admin Model
- `id`: Primary key
- `full_name`: Admin's full name
- `email`: Unique email address
- `password_hash`: Securely hashed password (using scrypt)
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp
- `opportunities`: Relationship to Opportunity records

#### Opportunity Model
- `id`: Primary key
- `title`: Opportunity name
- `duration`: Duration (e.g., "3 months")
- `start_date`: Start date string
- `description`: Full description
- `skills`: JSON array of skills
- `category`: Category (Technology, Business, etc.)
- `future_opportunities`: Future opportunity details
- `max_applicants`: Maximum number of applicants
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `admin_id`: Foreign key linking to creator (Admin)

---

## 🔒 Security Features

✅ **Password Security**
- Passwords hashed using Werkzeug's scrypt method
- Never stored or transmitted in plain text

✅ **Session Management**
- Flask-Login handles secure sessions
- "Remember Me" functionality with configurable duration
- HTTPOnly cookies

✅ **Input Validation**
- Email format validation
- Password strength requirements (minimum 8 characters)
- CSRF protection with session tokens
- All inputs sanitized to prevent HTML injection

✅ **Authentication & Authorization**
- Login required for sensitive operations (marked with `@login_required`)
- Users can only access their own opportunities
- Generic error messages to prevent email enumeration

✅ **Database Security**
- Foreign key constraints
- Indexed queries for performance
- Transaction management with rollback on errors

---

## 📝 API Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation successful",
  "data": { /* operation-specific data */ }
}
```

### Error Response
```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK`: Successful GET/POST request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate email or resource conflict
- `500 Internal Server Error`: Server error

---

## 🐛 Troubleshooting

### Virtual Environment Not Activating
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Port 5000 Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues
```bash
# Delete the database and let Flask recreate it
rm certifyme.db
python app.py
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---|---|
| POST | `/api/auth/signup` | No | Create new account |
| POST | `/api/auth/login` | No | Login to account |
| POST | `/api/auth/forgot` | No | Request password reset |
| POST | `/api/auth/logout` | Yes | Logout current user |
| GET | `/api/opportunities` | Yes | Get all user opportunities |
| POST | `/api/opportunities` | Yes | Create new opportunity |
| GET | `/api/opportunities/<id>` | Yes | Get opportunity details |
| PUT | `/api/opportunities/<id>/edit` | Yes | Update opportunity |
| DELETE | `/api/opportunities/<id>` | Yes | Delete opportunity |

---

## 🚀 Deployment Tips

For production deployment:
1. Set `DEBUG = False` in config.py
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set `SESSION_COOKIE_SECURE = True`
4. Use environment variables for sensitive config
5. Set proper CORS origins instead of `['*']`
6. Configure proper email sending for password resets
7. Use PostgreSQL instead of SQLite

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API response error messages
3. Check Flask server console for detailed error logs
4. Use browser DevTools Network tab to inspect API calls

---

## ✅ Completion Checklist

- ✅ Backend API fully functional
- ✅ Authentication system (signup, login, forgot password)
- ✅ CRUD operations for opportunities
- ✅ Frontend integrated with backend API calls
- ✅ Database models with proper relationships
- ✅ Error handling and validation
- ✅ Security best practices implemented
- ✅ API testing script included
- ✅ CORS enabled for development
- ✅ Session management working

**All tasks completed successfully!** 🎉


---

### ✅ Task 1 — Authentication *(Day 1)*

---

#### US-1.1 — Admin Sign Up

**Required Fields**
- Full Name
- Email
- Password
- Confirm Password

**Validations**
- All fields mandatory
- Email must be valid
- Password minimum 8 characters
- Passwords must match
- Email must be unique

**Expected Result**
- Save admin account
- Redirect to Login page

---

#### US-1.2 — Admin Login

**Fields**
- Email
- Password
- Remember Me checkbox

**Rules**
- Show generic error on failure:
  ```
  Invalid email or password
  ```

**Expected Result**
- Redirect to dashboard
- Load opportunities created by the admin

**Session Handling**

| Condition | Behaviour |
|---|---|
| Remember Me checked | Long-lived session |
| Remember Me unchecked | Session ends when browser closes |

---

#### US-1.3 — Forgot Password

**Requirements**
- Admin enters their email
- Always show the same success message (regardless of whether email exists)

**Behaviour**
- Generate reset link internally
- No email sending required

**Security**
- Reset link expires after **1 hour**
- Expired link shows an error

---

### ✅ Task 2 — Opportunity Management *(Day 2)*

> All opportunities must be stored in the database, linked to the logged-in admin, and must never use hardcoded data.

---

#### US-2.1 — View All Opportunities

**Each opportunity card must display:**
- Opportunity Name
- Category
- Duration
- Start Date
- Description

**Rules**
- Show only the logged-in admin's opportunities
- Remove all demo / hardcoded cards
- Show an empty state if no opportunities exist

---

#### US-2.2 — Add New Opportunity

**Required Fields**
- Opportunity Name
- Duration
- Start Date
- Description
- Skills to Gain *(comma separated)*
- Category
- Future Opportunities

**Optional Field**
- Maximum Applicants

**Category Options**
- Technology
- Business
- Design
- Marketing
- Data Science
- Other

**Expected Result**
- Validate all required fields
- Save opportunity to database
- Link opportunity to logged-in admin
- Display immediately **without page refresh**

---

#### US-2.3 — Opportunities Persist After Login

- Opportunities must load after logout / login cycles
- Stored only in the database — **no local storage usage**
- Admins cannot access other admins' data

---

#### US-2.4 — View Opportunity Details

- Open a details modal
- Show all saved fields
- Close button available

---

#### US-2.5 — Edit Opportunity

- Edit button opens a pre-filled form
- Apply the same validations as during creation
- Update only the selected opportunity
- Reflect changes instantly **without page refresh**

---

#### US-2.6 — Delete Opportunity

- Show a confirmation dialog before deletion
- Delete permanently from the database
- Remove from UI immediately **without page refresh**
- Only the creator admin can delete their own opportunity
