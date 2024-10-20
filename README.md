# AMS Auth Management

This repository manages the Backend for the AMS (Appointment Management System) project.

## Initial Folder Structure

```
AMS-USER-MANAGEMENT/
├── app/
│   ├── config/
|   |   └──configuration.py
│   ├── core/
|   |    ├──auth.py
|   |    └──const.py
│   ├── repository/
|   |    ├──user_repository.py
|   |    └──database.py
│   ├── routers/
|   |   └──api/
|   |      └──v1/
|   |         └──users.py
│   |── schemas/
|   |   └──users.py
│   ├── services/
|   |   └──users.py
│   ├── utils/
|   |    ├──email
|   |    |  └──send_email.py
|   |    └──helpers
|   |       └──converrters.py
│   |── Dockerfile
│   |── main.py
│   └── requirements.txt
├── __init__.py
├── docker-compose.yml
├── .gitignore
├── README.md
```

## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **fastapi**
- **uvicorn**
- **pymysql**
- **SQLAlchemy**

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd AMS-DATABASE-MANAGEMENT
   ```

2. **Set up the virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

### Docker Setup

#### 1. Create a `.env` file:

In the root directory (outside of the `app` folder), create a `.env` file with the following content:

```env
PROJECT_TITLE=AMS_AUTH_MANAGEMENT
BACKEND_PORT=8000
IS_RELOAD=True
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ams-database
JWT_SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=email@gmail.com
SMTP_PASSWORD=zzzz zzzz zzzz zzzz
FRONTEND_URL=http://your-frontend-url.com
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES=60
```

#### 2. Build and Run with Docker:

Use the following commands to build and run the Docker containers:

```bash
docker-compose build
docker-compose up
```

Alternatively, you can use:

```bash
docker-compose up --build
```

Visit the application at [http://localhost:8000/](http://localhost:8000/).
