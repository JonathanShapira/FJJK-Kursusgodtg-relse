# VibeCoding Django Backend

A Django backend with user profile management system.

## Features

- **User Authentication**: Login/logout system
- **User Profiles**: Extended user profiles with custom fields
- **Profile Management**: Users can edit their own profile information
- **REST API**: API endpoints for profile management
- **Admin Interface**: Django admin for user and profile management

## Custom Profile Fields

- **Træner for**: Trainer information
- **Reg nr**: Registration number
- **Konto nr**: Account number

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

## URLs

- **Home**: `http://localhost:8000/` (redirects to login or profile)
- **Login**: `http://localhost:8000/login/`
- **Register**: `http://localhost:8000/register/`
- **Profile Page**: `http://localhost:8000/profile/profile-page/`
- **Admin Interface**: `http://localhost:8000/admin/` (for superusers only)
- **API Endpoints**:
  - `GET /api/profile/` - Get user profile
  - `POST /api/profile/update/` - Update profile
  - `POST /api/user/update/` - Update user information
  - `GET /api/user-info/` - Get user information
  - `GET /api/profile-page-data/` - Get profile page data

## Usage

1. **Register**: Go to `/register/` to create a new account
2. **Login**: Go to `/login/` to login with your credentials
3. **Profile Page**: After login, you'll be automatically redirected to `/profile/profile-page/`
4. **Edit Profile**: Fill in the additional fields (Træner for, Reg nr, Konto nr) and click "Update Profile"
5. **Logout**: Click the logout link to return to the login page

## API Usage

The API endpoints require authentication. You can use the Django admin interface or make authenticated requests to the API endpoints.

### Example API Request

```javascript
// Get profile data
fetch('/api/profile-page-data/', {
    method: 'GET',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
    },
    credentials: 'same-origin'
})
.then(response => response.json())
.then(data => console.log(data));
```

## Models

### UserProfile
- `user`: One-to-one relationship with Django User
- `trainer_for`: CharField for trainer information
- `reg_number`: CharField for registration number
- `account_number`: CharField for account number
- `created_at`: DateTimeField (auto-created)
- `updated_at`: DateTimeField (auto-updated)

## Admin Features

- Custom User admin with inline profile editing
- Separate UserProfile admin for direct profile management
- Search and filter capabilities
- Read-only fields for timestamps
