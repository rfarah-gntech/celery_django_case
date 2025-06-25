# Swagger Documentation Setup

This project now includes Swagger/OpenAPI documentation for the API endpoints. Here's how to use it:

## Installation

If you're using Poetry for dependency management, run:

```bash
poetry add drf-yasg
```

If you're using pip, run:

```bash
pip install drf-yasg
```

Or if you're using Docker, rebuild your containers after the drf-yasg package has been added to pyproject.toml:

```bash
docker-compose build
docker-compose up
```

## Accessing the Swagger Documentation

After running the server, you can access the Swagger documentation at:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc UI: http://localhost:8000/redoc/
- JSON format: http://localhost:8000/swagger.json
- YAML format: http://localhost:8000/swagger.yaml

## Available Endpoints

The API provides the following endpoints:

### GET /stock/

Returns a list of all stock prices stored in the database.

### POST /stock/

Initiates an asynchronous task to generate a stock price. The task takes 60 seconds to complete.

**Request Body:**
```json
{
  "stock_name": "AAPL",
  "num_of_digits": 3
}
```

**Response:**
```json
{
  "message": "Task has been sent successfully!"
}
```

## Customizing the Documentation

You can further customize the Swagger documentation by modifying the view decorators in `stocks/views.py`.
