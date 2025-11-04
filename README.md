# String Analysis API


## Available Analyses

- **word_count**: Total number of words
- **char_count**: Total character count (including spaces)

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

## Installation

### Local Installation

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Docker Installation

1. **Build the Docker image**:
```bash
docker build -t string-analysis-api .
```

2. **Run the container**:
```bash
docker run -d -p 8000:8000 --name string-api string-analysis-api
```

## Usage

### Starting the Server

**Local development**:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Root Endpoint
```bash
GET /
```
Returns basic API information.

#### 2. Health Check
```bash
GET /health
```
Health check endpoint for monitoring.

#### 3. String Analysis (Main Endpoint)
```bash
POST /analyze
```

**Request Body** (JSON):
```json
{
  "text": "The quick brown fox jumps over the lazy dog!"
}
```

**Query Parameters** (optional):
- `analyses`: List of specific analyses to perform (can specify multiple)

**Examples**:

1. **Perform all analyses**:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world! This is a test."}'
```

2. **Request specific analyses**:
```bash
curl -X POST "http://localhost:8000/analyze?analyses=word_count&analyses=char_count" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world! This is a test."}'
```

**Response** (JSON):
```json
{
  "input_text": "Hello world! This is a test.",
  "input_length": 28,
  "analyses": {
    "word_count": 5,
    "char_count": 28
  }
}
```

#### 4. Get Available Analyses
```bash
GET /available-analyses
```
Returns a list of all available analysis types with descriptions.

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: Visit `http://localhost:8000/docs`
- **ReDoc**: Visit `http://localhost:8000/redoc`

These interfaces allow you to test the API directly from your browser!

## Testing

### Manual Testing

Use the interactive documentation at `/docs` or use curl/Postman.

### Example Test Cases

1. **Test with a palindrome**:
```bash
curl -X POST "http://localhost:8000/analyze?analyses=word_count" \
  -H "Content-Type: application/json" \
  -d '{"text": "A man a plan a canal Panama"}'
```

2. **Test input size limit**:
```bash
# This should return a 413 error if text exceeds MAX_INPUT_SIZE
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "'$(python -c 'print("a" * 10001)')'"}'
```

3. **Test invalid analysis type**:
```bash
curl -X POST "http://localhost:8000/analyze?analyses=invalid_analysis" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_INPUT_SIZE` | 10000 | Maximum allowed input size in characters |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8000 | Server port |
| `LOG_LEVEL` | INFO | Logging level |
| `CORS_ORIGINS` | * | Allowed CORS origins (configure for production) |
