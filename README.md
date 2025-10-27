# 🗣️ LiveKit Voice AI Agent

A production-ready, enterprise-grade conversational voice AI agent with multi-channel support, built on LiveKit Agents. Features modular prompt management, persistent memory, type-safe architecture, and seamless telephony integration for building intelligent voice assistants that work across web, mobile, and phone calls.

## 🎯 What This Project Does

This is a complete voice AI solution that enables natural, human-like conversations through:

* 🎙️ **Real-time Voice Conversations** - Low-latency speech-to-text, LLM processing, and text-to-speech pipeline
* 📞 **Multi-Channel Support** - Works on web browsers, mobile apps, and traditional phone calls (SIP/PSTN)
* 🧩 **Modular Prompt System** - JSON-based templates with Jinja2 rendering for easy customization
* 🧠 **Conversation Memory** - SQLite-backed persistent storage for user profiles and conversation history
* 🔧 **Configurable AI Providers** - Swap between multiple STT, LLM, and TTS providers (Deepgram, OpenAI, Anthropic, Cartesia, ElevenLabs, etc.)
* 🧾 **Type-Safe Architecture** - Pydantic models throughout for robust, maintainable code
* ✅ **Production Ready** - Ruff/Black formatted, comprehensive tests, CI/CD ready

## 👥 Who It's For

### Developers & Engineers
Build voice-enabled applications without starting from scratch. Perfect for:
* Creating AI phone assistants for businesses
* Adding voice interfaces to existing products
* Prototyping conversational AI solutions
* Learning modern AI agent architecture

### Businesses
Deploy intelligent voice agents for:
* **Customer Support** - 24/7 automated first-line support
* **Appointment Scheduling** - Healthcare, beauty, professional services
* **Lead Qualification** - Sales and marketing automation
* **Phone Receptionists** - Call routing and information gathering
* **Order Taking** - Restaurants, e-commerce, service bookings

### Industries
* 🏥 **Healthcare** - HIPAA-compliant appointment booking, patient triage
* 🏢 **Enterprise** - Internal helpdesk, HR assistance
* 🛍️ **E-commerce** - Order status, product inquiries
* 🏨 **Hospitality** - Hotel/restaurant reservations
* 📞 **Call Centers** - Automated tier-1 support

## ✨ Key Features

### Voice-to-LLM Real-time Interaction
Seamless audio streaming with natural conversation flow, voice activity detection, and turn-taking.

### Multi-Provider Flexibility
* **STT**: Deepgram, AssemblyAI, Groq, Azure, Google
* **LLM**: OpenAI, Anthropic, Groq, Google Gemini, Cerebras
* **TTS**: Cartesia, ElevenLabs, OpenAI, Azure, Google

### Intelligent Memory System
* User profile management
* Conversation history across sessions
* Context-aware responses
* Personalized interactions

### Enterprise-Grade Code Quality
* Type-safe with Pydantic models
* Black & Ruff formatted
* 80%+ test coverage
* Pre-commit hooks
* CI/CD ready

### Telephony Integration
* Inbound call handling (receive calls)
* Outbound calling (make calls)
* SIP trunk configuration
* Call routing and IVR

## Features

### 🗣️ Voice-to-LLM Real-time Interaction
- Low-latency streaming audio
- Natural conversation flow
- Voice Activity Detection (VAD)

### 🎙️ Multi-Provider Support
**STT:** Deepgram, AssemblyAI, Groq, Azure, Google  
**LLM:** OpenAI, Anthropic, Groq, Google, Cerebras  
**TTS:** Cartesia, ElevenLabs, OpenAI, Azure, Google

### 🧩 Modular Prompt System
- JSON-based prompt templates
- Jinja2 templating engine
- Organization-specific customization
- Version control for prompts

### 🧠 Multi-turn Memory
- SQLite-based conversation storage
- User profile management
- Conversation history retrieval
- Context-aware responses

### 🧾 Type-safe Architecture
- Pydantic models for all contexts
- Validated prompt variables
- Type hints throughout

voice-ai-project/
├── agent/
│   ├── agent_minimal_working.py  # Test the agent with minimal working options
│   ├── agent.py                  # Main agent
│   ├── model_selector.py         # Interactive selector
│── models/                       
│   ├── context.py                # Type-safe contexts
│   └── prompts.py                # Prompt models
│── prompts/                      
│   ├── manager.py                # Prompt manager
│   ├── renderer.py               # Jinja2 renderer
│   |── templates/                # JSON templates
│── memory/                       
│   ├── storage.py                # SQLite storage
│   └── conversation_memory.py    # Memory manager
|── telephony/                    # Phone support
├── tests/                        # Test suite
├── scripts/                      # Utility scripts
├── config/                       # SIP configs
|── data/                         # Database files
|── .env.example                  # Example env file
|── pyproject.toml                # Dependencies & config
└── requirements.txt              # Pip requirements

## Quick Start

### 1. Installation
```bash
pip install -e ".[dev]"
pre-commit install
python scripts/init_memory.py
```

### 2. Configuration

Copy `.env.example` to `.env` and place your own API keys into `.env`:
```bash
# LiveKit
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret

# AI Providers

# Model Selection (Options listed below)
STT_PROVIDER=deepgram  # Options: deepgram, assemblyai, groq, azure, google
LLM_PROVIDER=openai    # Options: openai, anthropic, groq, google, cerebras
TTS_PROVIDER=cartesia  # Options: cartesia, elevenlabs, openai, azure, google

# STT Configuration
STT_MODEL=nova-3                    # For Deepgram
STT_LANGUAGE=en                     # Language code
# ASSEMBLYAI_API_KEY=               # If using AssemblyAI
# GROQ_API_KEY=                     # If using Groq
# AZURE_SPEECH_KEY=                 # If using Azure
# AZURE_SPEECH_REGION=              # If using Azure

# LLM Configuration
LLM_MODEL=gpt-4o-mini              # Model name
# ANTHROPIC_API_KEY=                # If using Anthropic
# GROQ_API_KEY=                     # If using Groq
# GOOGLE_API_KEY=                   # If using Google
# CEREBRAS_API_KEY=                 # If using Cerebras

# TTS Configuration
TTS_VOICE=sonic-english            # Voice ID
TTS_MODEL=sonic-2                  # For Cartesia
# ELEVENLABS_API_KEY=               # If using ElevenLabs
# AZURE_SPEECH_KEY=                 # If using Azure

# Primary API Keys
OPENAI_API_KEY=
DEEPGRAM_API_KEY=
CARTESIA_API_KEY=

# SIP Trunk Configuration (for telephony)
SIP_TRUNK_ID=
SIP_OUTBOUND_TRUNK_ID=

### 3. Run Agent
```bash
# Console mode
python agent/agent.py console

# Development mode
python agent/agent.py dev

# Production mode
python agent/agent.py start
```

## Development

### Run Tests
```bash
pytest tests/ -v
```

### View Memory
```bash
python scripts/view_memory.py 
```

## Prompts

Create custom prompts in `prompts/templates/`:
```json
{
  "id": "custom_agent",
  "name": "Custom Agent",
  "template": "You are {{ role }} for {{ org_name }}...",
  "variables": [
    {
      "name": "role",
      "type": "string",
      "required": true
    }
  ]
}
```

## Telephony

### Setup SIP
```bash
python scripts/setup_sip.py
```

### Make Calls
```bash
python scripts/make_call.py +1234567890
```

## Testing
```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_prompts.py -v

## Deployment
```bash
# Build Docker image
docker build -t voice-ai-agent .

## Architecture

### Context Flow
```
User Input → STT → LLM (with context) → TTS → User Output
                    ↑
                    |
            [Agent Context]
            - User Profile
            - Conversation History
            - Organization Data
            - Rendered Prompt
```

### Memory System
```
Conversation → SQLite Storage
            ↓
    [User Profiles]
    [Message History]
    [Session Data]
```
## License

MIT