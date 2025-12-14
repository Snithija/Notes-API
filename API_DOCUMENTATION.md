# Public Notes API - Complete API Guide with JWT Authentication

## Overview

This is a complete Notes API with user authentication using JWT (JSON Web Tokens). Users must register, login to get tokens, and use those tokens to create and manage their notes.

---

## BASE URL

```
http://localhost:8000
```

---

## Authentication System

### Registration Endpoint

**POST** `/api/auth/register/`

Register a new user and get JWT tokens immediately.

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "password2": "SecurePassword123"
}
```

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**What happens:**

- User account is created
- Confirmation email sent to registered email
- JWT access and refresh tokens provided
- User can immediately use the access token to create notes

---

### Login Endpoint

**POST** `/api/auth/login/`

Login with existing credentials and get JWT tokens.

**Request Body:**

```json
{
  "username": "john_doe",
  "password": "SecurePassword123"
}
```

**Response (200 OK):**

```json
{
  "message": "You logged in successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**What happens:**

- User credentials validated
- Login confirmation email sent
- Fresh JWT tokens provided
- User can now access protected endpoints

---

## Notes API Endpoints

### All notes endpoints require JWT Authentication

Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### 1. List User's Notes

**GET** `/api/notes/`

Get all notes for the logged-in user.

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**

```json
{
  "message": "Your notes",
  "count": 2,
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "This is my first note",
      "user": "john_doe",
      "username": "john_doe",
      "created_at": "2025-12-14T10:30:00Z",
      "updated_at": "2025-12-14T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Second Note",
      "content": "Another note content",
      "user": "john_doe",
      "username": "john_doe",
      "created_at": "2025-12-14T11:00:00Z",
      "updated_at": "2025-12-14T11:00:00Z"
    }
  ]
}
```

**Important:** Users only see their own notes. If a user tries to view another user's notes or uses an invalid token, they get an error.

---

### 2. Create a New Note

**POST** `/api/notes/`

Create a new note for the logged-in user.

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "My New Note",
  "content": "This is the content of my new note. It can be any length."
}
```

**Response (201 Created):**

```json
{
  "message": "Note created successfully",
  "note": {
    "id": 3,
    "title": "My New Note",
    "content": "This is the content of my new note. It can be any length.",
    "user": "john_doe",
    "username": "john_doe",
    "created_at": "2025-12-14T12:00:00Z",
    "updated_at": "2025-12-14T12:00:00Z"
  }
}
```

**What happens:**

- Note is created and linked to the logged-in user
- Email confirmation sent to user's email
- Note is immediately available for viewing/editing

---

### 3. Get a Specific Note

**GET** `/api/notes/{id}/`

Retrieve a specific note (only if it belongs to the logged-in user).

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**URL Example:**

```
GET /api/notes/1/
```

**Response (200 OK):**

```json
{
  "message": "Note retrieved successfully",
  "note": {
    "id": 1,
    "title": "My First Note",
    "content": "This is my first note",
    "user": "john_doe",
    "username": "john_doe",
    "created_at": "2025-12-14T10:30:00Z",
    "updated_at": "2025-12-14T10:30:00Z"
  }
}
```

**Security:** If the note belongs to another user, returns 404 Not Found.

---

### 4. Update a Note

**PUT** `/api/notes/{id}/`

Update a specific note (only if it belongs to the logged-in user).

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**URL Example:**

```
PUT /api/notes/1/
```

**Request Body (all fields optional):**

```json
{
  "title": "Updated Title",
  "content": "Updated content goes here"
}
```

**Response (200 OK):**

```json
{
  "message": "Note updated successfully",
  "note": {
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content goes here",
    "user": "john_doe",
    "username": "john_doe",
    "created_at": "2025-12-14T10:30:00Z",
    "updated_at": "2025-12-14T13:00:00Z"
  }
}
```

---

### 5. Delete a Note

**DELETE** `/api/notes/{id}/`

Delete a specific note (only if it belongs to the logged-in user).

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**URL Example:**

```
DELETE /api/notes/1/
```

**Response (204 No Content):**

```json
{
  "message": "Note deleted successfully"
}
```

---

## JWT Token Details

### Access Token

- **Lifetime:** 1 day
- **Usage:** Include in Authorization header to access protected endpoints
- **Format:** Bearer `<token>`

### Refresh Token

- **Lifetime:** 7 days
- **Usage:** Use to get a new access token when current one expires
- **Endpoint:** POST `/api/token/refresh/` (if needed)

### Token Validation

- Invalid/expired tokens return **401 Unauthorized**
- Missing Authorization header returns **403 Forbidden**
- Invalid token format returns **401 Unauthorized**

---

## Security Features

### 1. User Isolation

- Each user can only see their own notes
- Trying to access another user's note returns 404
- Using another user's token shows "not valid user" error

### 2. Email Notifications

- Registration: Welcome email sent
- Login: Login confirmation email sent
- Create Note: Note creation notification email sent

### 3. Password Security

- Passwords are hashed using Django's security system
- Passwords must match during registration
- Minimum 8 characters required

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid credentials"
}
```

### 401 Unauthorized (Invalid/Missing Token)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found (Note not found or belongs to another user)

```json
{
  "detail": "Not found."
}
```

---

## Complete Usage Example

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "password2": "SecurePassword123"
  }'

# Get access token from response
TOKEN="<access_token_from_response>"

# 2. Create a note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "My First Note",
    "content": "Note content here"
  }'

# 3. View all notes
curl -X GET http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Get specific note
curl -X GET http://localhost:8000/api/notes/1/ \
  -H "Authorization: Bearer $TOKEN"

# 5. Update a note
curl -X PUT http://localhost:8000/api/notes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content"
  }'

# 6. Delete a note
curl -X DELETE http://localhost:8000/api/notes/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Email Configuration

The API is configured to send emails using Gmail SMTP.

**Settings:**

- Email Host: smtp.gmail.com
- Port: 587
- TLS: Enabled
- From Email: snithijaraavi25@gmail.com

**Events that trigger emails:**

1. User Registration - Welcome email
2. User Login - Login confirmation email
3. Create Note - Note creation notification

---

## Database

- **Type:** SQLite (db.sqlite3)
- **User Model:** Django's built-in User model with email field
- **Note Model:** Custom model with ForeignKey to User

---

## How to Run

1. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

2. **Server runs at:**

   ```
   http://localhost:8000
   ```

3. **Test the API using curl or Postman with the examples above**

---

## Key Features Summary

✅ User Registration with Email Notification  
✅ User Login with JWT Tokens  
✅ Create Notes (POST)  
✅ View Own Notes (GET)  
✅ Update Notes (PUT)  
✅ Delete Notes (DELETE)  
✅ JWT Token Validation  
✅ User Isolation (can't see other users' notes)  
✅ Email Notifications on Important Events  
✅ Secure Password Hashing  
✅ Token Refresh Support

---

**API Status:** Ready for testing!
