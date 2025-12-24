# WromGPT Quick Deployment Guide

This guide helps you deploy WromGPT to various platforms.

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:8000/docs

## ☁️ Deployment Options

### 1. Heroku
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-wromgpt-app

# Deploy
git push heroku main

# Set environment (optional)
heroku config:set MODEL_NAME=gpt2
```

### 2. Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment in dashboard
# Add MODEL_NAME variable
```

### 3. Docker
```bash
# Build and run
docker-compose up -d

# Or build manually
docker build -t wromgpt .
docker run -p 8000:8000 -e MODEL_NAME=gpt2 wromgpt
```

### 4. Google Cloud
```bash
# Deploy to App Engine
gcloud app deploy app.yaml

# Set environment
gcloud app deploy --set-env-vars MODEL_NAME=gpt2
```

### 5. Railway
1. Connect GitHub repository
2. Deploy automatically
3. Set MODEL_NAME in environment variables

### 6. Render
1. Connect GitHub repository
2. Choose "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 🔧 Configuration

### Environment Variables
- `MODEL_NAME`: Hugging Face model (default: "gpt2")
- `PORT`: Server port (default: 8000)

### Recommended Models
- `gpt2` - Small, fast (124M params)
- `distilgpt2` - Smaller, faster
- `gpt2-medium` - Better quality (355M params)
- `gpt2-large` - Best quality (774M params)

## 📝 Testing

### Using the example client
```bash
python example_client.py
```

### Using cURL
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

## 📚 Documentation
- API Docs: `/docs`
- ReDoc: `/redoc`
- Full README: See README.md

## 💡 Tips
1. Use smaller models (gpt2, distilgpt2) for faster responses
2. GPU-enabled hosting improves performance
3. Monitor memory usage - larger models need more RAM
4. Set custom instructions for specialized use cases
5. Use the /health endpoint for monitoring

## 🔒 Security Notes
- Thread-safe instruction updates
- No security vulnerabilities detected
- Consider adding authentication for production
- Rate limiting recommended for public APIs

## 🆘 Troubleshooting

### Model won't load
- Check internet connection (first run downloads model)
- Verify MODEL_NAME is correct
- Try smaller model like "distilgpt2"

### Out of memory
- Use smaller model
- Reduce max_length in requests
- Deploy to instance with more RAM

### Slow responses
- Use GPU-enabled hosting
- Try distilgpt2 model
- Reduce max_length parameter

## 📞 Support
For issues, see the full README.md or open a GitHub issue.
