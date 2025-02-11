# 🌍 Geolocation API

A FastAPI-based service that allows users to store, retrieve, and delete geolocation data based on IP addresses or domain names. The project integrates with the [IPStack API](https://ipstack.com/) for geolocation lookups and uses PostgreSQL as the database.

## 🚀 Features

- 🌎 Fetch geolocation data for an IP address or domain
- 📌 Store geolocation records in a PostgreSQL database
- 🔍 Retrieve geolocation data by IP, domain, or unique ID
- 🗑️ Delete geolocation records by ID
- 🏗️ Fully containerized using **Docker & Docker Compose**
- 📜 OpenAPI documentation (FastAPI's automatic docs)
- ✅ Unit and integration tests using **pytest & HTTPX**

## 🛠️ Technologies Used

- **Python 3.12**
- **FastAPI** – for building the API
- **SQLAlchemy & Alembic** – for database management and migrations
- **PostgreSQL** – as the database
- **asyncpg** – async database driver
- **httpx** – for async HTTP requests to IPStack
- **Docker & Docker Compose** – for containerization
- **pytest & pytest-asyncio** – for testing

---

## 📦 Installation

### 1️⃣ Clone the repository

```sh
git clone https://github.com/adrian-ska/geolocation-api.git
cd geolocation-api
```

### 2️⃣ Set up the virtual environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

### 3️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root with the following content:

```ini
DATABASE_URL=postgresql+asyncpg://user:password@db/geolocation_db
IPSTACK_API_KEY=your_api_key_here
LOGGER_LEVEL=INFO
BASE_URL=http://api.ipstack.com
```

---

## 🐳 Running with Docker

Ensure **Docker** and **Docker Compose** are installed, then run:

```sh
docker-compose up --build
```

This will start:

- The **FastAPI** app on `http://127.0.0.1:8000`
- A **PostgreSQL** database

Once running, apply database migrations:

```sh
docker-compose exec app alembic upgrade head
```

---

## 📝 API Endpoints

### 📍 Add geolocation (POST)

```http
POST /geolocation
```

#### Request body:

```json
{
  "ip_or_url": "8.8.8.8"
}
```

### 🔍 Retrieve geolocation by IP or URL (GET)

```http
GET /geolocation?ip_or_url=8.8.8.8
```

### 🔍 Retrieve geolocation by ID (GET)

```http
GET /geolocation?id=4
```

### 📋 Retrieve all geolocations (GET)

```http
GET /geolocation/
```

### 🗑️ Delete geolocation by ID (DELETE)

```http
DELETE /geolocation/2
```

📜 **For full API documentation, visit:**  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ✅ Running Tests

To run the test suite, use:

```sh
pytest
```

To test in Docker:

```sh
docker-compose exec app pytest
```

## Author:
Adrian Skawinski

email: adrian.skawinski@gmail.com
