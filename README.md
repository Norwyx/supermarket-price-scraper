# Supermarket Price Scraper

Backend project for scraping supermarket prices, built with FastAPI, SQLModel, and PostgreSQL.

## Project Structure

```
backend/
├── app/
│   ├── core/           # Core logic (settings, security, etc.)
│   ├── models/         # Database models (SQLModel)
│   ├── routers/        # API endpoints
│   ├── __init__.py
│   ├── config.py       # Environment variables configuration
│   ├── database.py     # Database configuration
│   └── main.py         # Application entry point
├── .gitignore          # Git ignore file
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## Installation Guide

Follow these steps to set up your local development environment.

### 1. Prerequisites

Ensure you have installed:
- Python 3.10+
- PostgreSQL

### 2. Set up Virtual Environment

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file with your database credentials if they differ from the defaults.

### 5. Setup Database (Supabase)

1.  **Create a Project**: Go to [Supabase](https://supabase.com/) and create a new project.
2.  **Get Connection String**:
    *   Go to `Project Settings` -> `Database`.
    *   Under `Connection string`, select `URI`.
    *   Copy the connection string. It will look like: `postgresql://postgres.[ref]:[password]@...`
3.  **Update .env**:
    *   Paste the connection string into your `.env` file as `DATABASE_URL`.
    *   Replace `[YOUR-PASSWORD]` with your actual database password.

*Note: You don't need to run `createdb` locally since Supabase provides the database.*

### 6. Run the Server

```bash
uvicorn app.main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.
You can view the interactive documentation at `http://127.0.0.1:8000/docs`.
