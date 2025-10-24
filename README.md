![AI ChatBot](img/ai-chatbot.png)

Intelligent Telegram bot with automatic document indexing and vector-based question answering using OpenAI GPT-4 and Pinecone. The bot monitors a local documents folder in real-time and automatically updates its knowledge base when files are added, modified, or deleted.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Docker Deployment](#docker-deployment)
- [Health Check](#health-check)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automatic Document Indexing** - Real-time monitoring and indexing of `.txt`, `.pdf`, `.docx` files using Watchdog
- **Vector Search** - Semantic search using OpenAI embeddings (text-embedding-ada-002) and Pinecone vector database
- **Intelligent Question Answering** - Context-aware responses powered by GPT-4 with source citations
- **Telegram Bot Interface** - User-friendly chat interface with command support
- **REST API** - HTTP endpoints for programmatic access and integrations
- **Real-time Updates** - Automatic knowledge base synchronization when documents change
- **Conversation Memory** - Maintains chat history per user for contextual conversations
- **Docker Ready** - Fully containerized with Docker Compose for easy deployment

## Architecture

```
ai-chatbot/
├── README.md                            # Documentation
├── .env.example                         # Environment template
├── requirements.txt                     # Dependencies
├── src/                                 # Source code
│   ├── main.py                          # Application entry point
│   ├── core/                            # Core configuration
│   │   ├── config.py                    # Settings management
│   │   ├── logger.py                    # Logging configuration
│   │   └── exceptions.py                # Custom exceptions
│   ├── services/                        # Business logic
│   │   ├── llm/                         # Language models
│   │   │   ├── base.py                  # Abstract interface
│   │   │   └── openai_service.py        # OpenAI implementation
│   │   ├── knowledge/                   # Knowledge management
│   │   │   ├── document_loader.py       # Document reading
│   │   │   ├── chunker.py               # Text chunking
│   │   │   └── retriever.py             # Information retrieval
│   │   └── memory/                      # Conversation management
│   │       └── conversation_memory.py   # Chat history
│   ├── vectorstore/                     # Vector database
│   │   ├── pinecone_store.py            # Pinecone integration
│   │   └── indexer.py                   # Document indexing
│   ├── bot/                             # Telegram bot
│   │   ├── dispatcher.py                # Bot lifecycle
│   │   └── handlers/                    # Message handlers
│   │       ├── message_handler.py       # Text processing
│   │       └── command_handler.py       # Bot commands
│   └── api/                             # REST API
│       ├── app.py                       # FastAPI application
│       └── routes/                      # API endpoints
│           ├── health.py                # Health check
│           └── chat.py                  # Query endpoint
├── tests/                               # Test suite
│   ├── conftest.py                      # Pytest configuration
│   └── unit/
│       └── test_chunker.py              # Unit tests
├── scripts/                             # Utility scripts
│   ├── setup.py                         # Initial setup
│   └── index_documents.py               # Manual indexing
├── deploy/docker/                       # Docker files
│   ├── Dockerfile                       # Container image
│   └── docker-compose.yml               # Multi-container setup
├── data/documents/                      # Documents folder
└── logs/                                # Application logs
```

## Prerequisites

### Required Software

- **Python 3.11 or higher**
- **pip** (Python package manager)
- **Docker** and **Docker Compose** (for containerized deployment)

### System Requirements

- **RAM**: Minimum 2GB, recommended 4GB
- **Storage**: 1GB free space for application and logs
- **Network**: Stable internet connection for API calls

### Required API Keys

1. **Telegram Bot Token**
   - Create a bot via [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow instructions
   - Save the token provided

2. **OpenAI API Key**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Navigate to API Keys section
   - Create new secret key
   - Ensure you have credits available

3. **Pinecone Account**
   - Sign up at [Pinecone](https://www.pinecone.io/)
   - Create a new project 
   - Create an index with dimension 2048
   - Get API key from dashboard
   - Note your environment region

## Local Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/NadiiaBCN/ai-chatbot
cd ai-chatbot
```

### Step 2: Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
nano .env
```

Required environment variables:

```bash
# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token-here

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here
PINECONE_INDEX_NAME=your_index-name_here
```

### Step 5: Run Setup Script

```bash
python scripts/setup.py
```

This script will:
- Create necessary directories (`data/documents`, `logs`)
- Validate environment configuration
- Check for required API keys

### Step 6: Add Documents

```bash
# Add your documents to the monitored folder
cp /path/to/your/documents/*.pdf data/documents/
cp /path/to/your/documents/*.txt data/documents/
cp /path/to/your/documents/*.docx data/documents/
```

Supported formats:
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.docx` - Microsoft Word documents

### Step 7: Start Application

```bash
# Start all services (Bot + API + Indexer)
python -m src.main
```

### Step 8: Test the Bot

1. Open Telegram and find your bot
2. Send `/start` to initialize
3. Ask a question about your documents

Example:
```
You: What are healthy eating tips?

Bot: Based on our knowledge base, healthy eating tips include:
- Consume at least 5 servings of fruits and vegetables daily
- Choose whole grain cereals
- Include legumes regularly

📚 Sources:
• Healthy_Eating_Plate.docx
• RECOMENDACIONES_DIETETICAS_EN.pdf

✓ Confidence: 87%
```

## Docker Deployment

### Step 1: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

### Step 2: Configure Document Mounting

1. **Setup environment:**
```bash
cp .env.example .env
nano .env  # Add your API keys
```

2. **Configure documents folder:**

If your project structure is:
```
ai-chatbot/
├── data/documents/     # Your documents here
└── deploy/docker/
```

Then **no changes needed** - `docker-compose.yml` already uses relative paths.

If you want to use a **different folder**, edit `deploy/docker/docker-compose.yml`:
```yaml
volumes:
  - /your/custom/path:/app/data/documents
```

### Step 3: Build and Start

```bash
cd deploy/docker
docker-compose up -d --build
```

### Step 4: Verify Deployment

```bash
# Check container status
docker-compose ps

# Expected output:
# NAME        STATUS          PORTS
# ai-chatbot  Up 30 seconds   0.0.0.0:8000->8000/tcp

```

## Health Check

### HTTP Endpoint

```bash
# Check application health
curl http://localhost:8000/health
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_connected": true
}
```

### Bot Command

Use `/status` command in Telegram:

```
🤖 Bot Status

Vector Database: ✅ Online
Version: 1.0.0

✓ Ready to answer questions!
```

### Application Logs

**View logs in real-time:**

```bash
# Local deployment
tail -f logs/app_*.log

# Docker deployment
docker-compose logs -f chatbot
```

## Troubleshooting

### Bot Not Responding

**Solutions:**

1. **Check bot token:**
   ```bash
   grep TELEGRAM_BOT_TOKEN .env
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   ```

2. **Check bot is running:**
   ```bash
   # Local
   ps aux | grep "python -m src.main"
   
   # Docker
   docker-compose ps
   ```

3. **Restart bot:**
   ```bash
   # Docker
   docker-compose restart chatbot
   ```

### Documents Not Being Indexed

**Solutions:**

1. **Check file format:**
   ```bash
   # Only .txt, .pdf, .docx are supported
   ls -la data/documents/
   ```

2. **Manual reindex:**
   ```bash
   # Docker
   docker-compose exec chatbot python scripts/index_documents.py
   ```

### Pinecone Connection Errors

**Solutions:**

1. **Verify API key:**
   ```bash
   grep PINECONE_API_KEY .env
   ```

2. **Check Pinecone status:**
   - Visit [Pinecone Status Page](https://status.pinecone.io/)

## Contributing

Contributions are welcome! Please follow the code style guidelines:

- **Follow PEP 8** - Python's official style guide
- **Add docstrings to all functions** - Include Args, Returns, and Raises sections
- **Write tests for new features** - Maintain >80% code coverage
- **Update documentation** - Keep README.md current with changes

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit: `git commit -m "Add: amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

MIT License - See LICENSE file for details