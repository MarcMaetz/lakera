# Content Moderation Service

A simple content moderation service that uses the KoalaAI/Text-Moderation model from Hugging Face to classify text content.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Install development dependencies (for testing):
```bash
pip install -e ".[dev]"
```

4. Run the service:
```bash
python run.py
```

The service will be available at `http://localhost:8000`

## API Usage

### Moderate Text
Send a POST request to `/moderate` with a JSON body containing the text to moderate:

```bash
curl -X POST "http://localhost:8000/moderate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text to moderate here"}'
```

The response will include moderation scores for each category.

### Health Check
Check the service health:

```bash
curl "http://localhost:8000/health"
```

## Development

### Running Tests
```bash
pytest src/tracking/test_request_tracker.py -v
```

### Project Structure
```
src/
├── moderation/
│   ├── controller.py    # FastAPI routes
│   ├── models.py        # Pydantic models
│   └── service.py       # Business logic
├── tracking/
│   ├── request_tracker.py    # Request tracking
│   └── test_request_tracker.py
├── utils/
│   └── logger.py
└── config.py
```

## Production Considerations

For a production MVP, consider:

1. **Monitoring & Logging**
   - Implement proper logging with rotation
   - Add health check endpoints
   - Consider using Prometheus/Grafana for metrics

2. **Performance**
   - Add caching for frequent requests
   - Consider model quantization for faster inference
   - Implement request batching

3. **Security**
   - Add authentication/authorization
   - Rate limiting
   - Input validation and sanitization

4. **Reliability**
   - Error handling and retries
   - Model versioning
   - Backup and recovery procedures

5. **Deployment**
   - Containerization (Docker)
   - CI/CD pipeline
   - Load balancing
   - Auto-scaling configuration 