# 🧠 Stack Overflow Clone (Backend API)

A full-featured, production-ready Django REST API inspired by Stack Overflow — with users, questions, answers, voting, notifications, and JWT authentication.

---

## 🚀 Features

- ✅ **User Registration & JWT Login**
- ✅ **Post, update, delete Questions & Answers**
- ✅ **Upvote/Downvote system**
- ✅ **Accept Answer feature**
- ✅ **Notification System** (new answer, accepted answer)
- ✅ **Pagination, Filtering, Search**
- ✅ **RESTful, Class-Based Views (DRF ViewSets)**
- ✅ **OOP Architecture**: services, serializers, modular folders
- ✅ **Tested with DRF’s APITestCase**

---

## 🧰 Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL (or SQLite for dev)
- SimpleJWT
- `.env` config via `django-environ`
- DRF ViewSets, Routers, GenericAPIView

---

## 📁 Project Structure

```
apps/
├── users/          # Auth, profile
├── questions/      # Questions, votes
├── answers/        # Answers, accept logic
├── notifications/  # New answer & acceptance alerts
core/
    └── settings/   # base.py, dev.py, prod.py
```

---

## 🔐 .env Configuration

Create a `.env` file at the root:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=PostgreSQL:///db.sqlite3  # Or PostgreSQL URL
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🧪 Running Locally

```bash
# Create & activate virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```

---

## 🔑 Auth & JWT

Obtain token:
```
POST /api/token/
{
  "username": "your_user",
  "password": "your_pass"
}
```

Use returned token as:
```
Authorization: Bearer <access_token>
```

---

## 🔁 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST   | `/api/register/`       | Register a user |
| POST   | `/api/token/`          | Get JWT token |
| GET    | `/api/profile/`        | User profile |
| CRUD   | `/api/questions/`      | Manage questions |
| CRUD   | `/api/answers/`        | Manage answers |
| POST   | `/api/answers/<id>/accept/` | Accept answer |
| POST   | `/api/questions/<id>/vote/` | Vote question |
| POST   | `/api/answers/<id>/vote/`   | Vote answer |
| GET    | `/api/notifications/`  | View notifications |
| PATCH  | `/api/notifications/<id>/read/`  | View notifications |

---

## 🧪 Running Tests

```bash
python manage.py test
```

Tests include:
- Authentication
- Question/Answer logic
- Voting system
- Notifications
- Permissions & filtering

## 🧪 Postman Collection

[<img src="https://run.pstmn.io/button.svg" alt="Run in Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/21311841-e63fb6a6-3b98-414a-9d96-a9b2391861f2?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D21311841-e63fb6a6-3b98-414a-9d96-a9b2391861f2%26entityType%3Dcollection%26workspaceId%3Dd1b9a31e-eb74-4e8b-93be-36bdf4641056)

Click the button above to instantly import and test the full API in Postman — includes auth, questions, answers, voting, and notifications.


## 🧑‍💻 Contributors

- Waqar Yaqoob

---

## 📦 Deployment (Next Step)

Project link:
- 🔵 https://stack-overflow-r98k.onrender.com/api/questions/

---

## 📄 License

Thank You!
