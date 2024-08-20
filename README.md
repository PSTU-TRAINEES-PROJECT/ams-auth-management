# AMS Database Management

This repository manages the Backend for the AMS (Appointment Management System) project.

## Initial Folder Structure

```
AMS-DATABASE-MANAGEMENT/
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
