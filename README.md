# WromGPT API

A powerful GPT-based AI assistant API with instruction injection capabilities, built with FastAPI and Hugging Face Transformers.

## Features

- 🤖 Hugging Face GPT model integration
- 💉 Custom instruction injection system
- 🚀 Fast and efficient FastAPI backend
- 🌐 RESTful API endpoints
- ☁️ Deploy anywhere (Vercel, Heroku, or any cloud platform)
- 🔧 Configurable model selection
- 📝 Dynamic instruction updates

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/RecklessEvadingDriver/testgot.git
   cd testgot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**
   - API docs: http://localhost:8000/docs
   - API: http://localhost:8000

## API Endpoints

### 1. Root Endpoint
```http
GET /
```
Returns API information and available endpoints.

**Response:**
```json
{
  "name": "WromGPT API",
  "version": "1.0.0",
  "status": "running",
  "ai_model": "wromgpt",
  "model": "gpt2",
  "endpoints": {
    "chat": "/api/chat",
    "instructions": "/api/instructions",
    "health": "/health"
  }
}
```

### 2. AI Model Info
```http
GET /ai/model
```
Returns the logical AI model identifier used by WromGPT and the underlying Hugging Face model name.

**Response:**
```json
{
  "ai_model": "wromgpt",
  "model_name": "gpt2"
}
```

### 3. Health Check
```http
GET /health
```
Check if the service and model are loaded properly.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "gpt2"
}
```

### 4. Chat Endpoint
```http
POST /api/chat
```
Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "What is artificial intelligence?",
  "max_length": 200,
  "temperature": 0.7,
  "custom_instructions": "You are a technical expert."
}
```

**Response:**
```json
{
  "response": "Artificial intelligence (AI) is...",
  "model_used": "gpt2"
}
```

**Parameters:**
- `message` (required): The user's message
- `max_length` (optional): Maximum length of response (default: 200)
- `temperature` (optional): Sampling temperature (default: 0.7)
- `custom_instructions` (optional): Custom instructions for this conversation

### 5. Get System Instructions
```http
GET /api/instructions
```
Retrieve the current system instructions.

**Response:**
```json
{
  "instructions": "You are WromGPT, a helpful..."
}
```

### 6. Update System Instructions
```http
POST /api/instructions
```
Update the system instructions that are injected into all conversations.

**Request Body:**
```json
{
  "instructions": "You are a specialized assistant for..."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "System instructions updated",
  "instructions": "You are a specialized assistant for..."
}
```

## Deployment

### Deploy to Heroku

1. **Install Heroku CLI** (if not already installed)
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create a new Heroku app**
   ```bash
   heroku create your-wromgpt-app
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Set environment variables (optional)**
   ```bash
   heroku config:set MODEL_NAME=gpt2
   ```

### Deploy to Vercel

1. **Install Vercel CLI** (if not already installed)
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set environment variables (optional)**
   - Go to your project settings on Vercel dashboard
   - Add `MODEL_NAME` environment variable

### Deploy to Other Platforms

The application can be deployed to any platform that supports Python applications:

- **AWS Lambda**: Use Mangum adapter
- **Google Cloud Run**: Use the Dockerfile approach
- **Azure App Service**: Deploy as Python web app
- **Railway**: Connect your GitHub repo
- **Render**: Connect your GitHub repo

## Configuration

### Environment Variables

- `MODEL_NAME`: Hugging Face model to use (default: "gpt2")
  - Examples: "gpt2", "gpt2-medium", "gpt2-large", "distilgpt2"
- `AI_MODEL`: Logical AI model identifier exposed by the API (default: "wromgpt")
- `PORT`: Port to run the server (default: 8000)

### Changing the Model

You can use any compatible Hugging Face model by setting the `MODEL_NAME` environment variable:

```bash
export MODEL_NAME=gpt2-medium
python app.py
```

Recommended models:
- `gpt2` (small, fast, 124M parameters)
- `gpt2-medium` (355M parameters)
- `gpt2-large` (774M parameters)
- `distilgpt2` (smaller and faster)

## Usage Examples

### Using cURL

**Chat request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

**Update instructions:**
```bash
curl -X POST "http://localhost:8000/api/instructions" \
  -H "Content-Type: application/json" \
  -d '{"instructions": "You are a helpful coding assistant."}'
```

### Using Python

```python
import requests

# Chat with the AI
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Explain quantum computing",
        "max_length": 150,
        "temperature": 0.8
    }
)
print(response.json())
```

### Using JavaScript

```javascript
// Chat with the AI
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What is machine learning?',
    max_length: 200,
    temperature: 0.7
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Requirements

- Python 3.11+
- FastAPI
- Transformers (Hugging Face)
- PyTorch
- Uvicorn

See `requirements.txt` for complete list of dependencies.

## Architecture

```
WromGPT
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku configuration
├── runtime.txt        # Python version for Heroku
├── vercel.json        # Vercel configuration
└── README.md          # Documentation
```

## Features in Detail

### Instruction Injection

The core feature of WromGPT is instruction injection. Every conversation can have:
1. **System Instructions**: Global instructions that apply to all conversations
2. **Custom Instructions**: Per-request instructions that override system instructions

This allows you to:
- Set the AI's personality and behavior
- Define specific roles (e.g., "technical expert", "creative writer")
- Enforce guidelines and constraints
- Customize responses for different use cases

### Model Flexibility

Use any Hugging Face model compatible with the `AutoModelForCausalLM` class:
- GPT models
- GPT-2 variants
- GPT-Neo
- GPT-J
- And many more

## Troubleshooting

### Model Loading Issues

If the model fails to load:
1. Check your internet connection (first run downloads the model)
2. Verify the model name is correct
3. Ensure you have enough disk space
4. Try a smaller model like "distilgpt2"

### Memory Issues

If you encounter out-of-memory errors:
1. Use a smaller model (e.g., "distilgpt2" instead of "gpt2")
2. Reduce `max_length` in requests
3. Deploy to a platform with more RAM

### Performance Optimization

For better performance:
1. Use a GPU-enabled environment
2. Use smaller models for faster response times
3. Implement caching for common queries
4. Use model quantization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] Add authentication
- [ ] Implement rate limiting
- [ ] Add conversation history
- [ ] Support for multiple models simultaneously
- [ ] WebSocket support for streaming responses
- [ ] Fine-tuning capabilities
- [ ] Model caching and optimization

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)
