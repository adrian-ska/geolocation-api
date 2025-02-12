# Geolocation API

This is a FastAPI-based service for storing, retrieving, and deleting geolocation data based on IP addresses or domain names. The project integrates with the [IPStack API](https://ipstack.com/) for geolocation lookups and uses PostgreSQL as the database.

## Features

- Retrieve geolocation data for an IP address or domain
- Store geolocation records in a PostgreSQL database
- Retrieve geolocation data by IP, domain, or unique ID
- Delete geolocation records by ID
- Containerized using **Docker & Docker Compose**
- OpenAPI documentation available via FastAPI
- Unit and integration tests using **pytest & HTTPX**

## Technologies Used

- **Python 3.12**
- **FastAPI** – API framework
- **SQLAlchemy & Alembic** – Database management and migrations
- **PostgreSQL** – Database
- **asyncpg** – Async database driver
- **httpx** – HTTP client for API requests
- **Docker & Docker Compose** – Containerization
- **pytest & pytest-asyncio** – Testing

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/adrian-ska/geolocation-api.git
cd geolocation-api
```

### 2. Set up the virtual environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```ini
DATABASE_URL=postgresql+asyncpg://user:password@db/geolocation_db
IPSTACK_API_KEY=your_api_key_here
LOGGER_LEVEL=INFO
BASE_URL=http://api.ipstack.com
```

Alternatively, if a `env.example` file is provided, you can copy it:

```sh
mv env.example .env  # On Linux/macOS
```

Then, update the `.env` file with your actual database credentials and API key.

### Changing the Database Configuration

If you want to use a different database, update the `DATABASE_URL` in the `.env` file and also modify the `sqlalchemy.url` setting in `alembic.ini` accordingly.

## Running with Docker

Ensure **Docker** and **Docker Compose** are installed, then run:

```sh
docker-compose up --build
```

This will start:

- The FastAPI application at `http://127.0.0.1:8000`
- A PostgreSQL database

Once running, apply database migrations:

```sh
docker-compose exec app alembic upgrade head
```

## API Endpoints

### Add geolocation (POST)

```http
POST /geolocation
```

#### Request body:

```json
{
  "ip_or_url": "8.8.8.8"
}
```

### Retrieve geolocation by IP or URL (GET)

```http
GET /geolocation?ip_or_url=8.8.8.8
```

### Retrieve geolocation by ID (GET)

```http
GET /geolocation?id=4
```

### Retrieve all geolocations (GET)

```http
GET /geolocation/
```

### Delete geolocation by ID (DELETE)

```http
DELETE /geolocation/2
```

For full API documentation, visit:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

To run tests:

```sh
pytest
```

To test in Docker:

```sh
docker-compose exec app pytest
```

## Author

Adrian Skawinski  
Email: adrian.skawinski@gmail.com

