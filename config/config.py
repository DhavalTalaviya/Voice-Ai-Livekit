import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for AI models"""
    
    # STT Configuration
    stt_provider: str = "deepgram"
    stt_model: str = "nova-3"
    stt_language: str = "en"
    
    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    
    # TTS Configuration
    tts_provider: str = "cartesia"
    tts_model: str = "sonic-2"
    tts_voice: str = "sonic-english"
    
    @classmethod
    def from_env(cls) -> "ModelConfig":
        """Create config from environment variables"""
        return cls(
            stt_provider=os.getenv("STT_PROVIDER", "deepgram"),
            stt_model=os.getenv("STT_MODEL", "nova-3"),
            stt_language=os.getenv("STT_LANGUAGE", "en"),
            llm_provider=os.getenv("LLM_PROVIDER", "openai"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            tts_provider=os.getenv("TTS_PROVIDER", "cartesia"),
            tts_model=os.getenv("TTS_MODEL", "sonic-2"),
            tts_voice=os.getenv("TTS_VOICE", "sonic-english"),
        )
    
    def get_stt_descriptor(self) -> str:
        """Get STT model descriptor for LiveKit Inference"""
        return f"{self.stt_provider}/{self.stt_model}:{self.stt_language}"
    
    def get_llm_descriptor(self) -> str:
        """Get LLM model descriptor for LiveKit Inference"""
        return f"{self.llm_provider}/{self.llm_model}"
    
    def get_tts_descriptor(self) -> str:
        """Get TTS model descriptor for LiveKit Inference"""
        return f"{self.tts_provider}/{self.tts_model}"


# Available providers
STT_PROVIDERS = {
    "deepgram": {
        "models": ["nova-3", "nova-2", "base"],
        "languages": ["en", "multi", "es", "fr", "de", "pt", "it"],
        "requires_key": "DEEPGRAM_API_KEY",
    },
    "assemblyai": {
        "models": ["universal-streaming", "nano", "best"],
        "languages": ["en", "multi"],
        "requires_key": "ASSEMBLYAI_API_KEY",
    },
    "groq": {
        "models": ["whisper-large-v3", "distil-whisper-large-v3-en"],
        "languages": ["en", "multi"],
        "requires_key": "GROQ_API_KEY",
    },
    "azure": {
        "models": ["default"],
        "languages": ["en", "es", "fr", "de", "pt", "it"],
        "requires_key": "AZURE_SPEECH_KEY",
    },
    "google": {
        "models": ["chirp-2"],
        "languages": ["en", "multi"],
        "requires_key": "GOOGLE_API_KEY",
    },
}

LLM_PROVIDERS = {
    "openai": {
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        "requires_key": "OPENAI_API_KEY",
    },
    "anthropic": {
        "models": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"],
        "requires_key": "ANTHROPIC_API_KEY",
    },
    "groq": {
        "models": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        "requires_key": "GROQ_API_KEY",
    },
    "google": {
        "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro"],
        "requires_key": "GOOGLE_API_KEY",
    },
    "cerebras": {
        "models": ["llama-3.3-70b", "llama-3.1-8b"],
        "requires_key": "CEREBRAS_API_KEY",
    },
}

TTS_PROVIDERS = {
    "cartesia": {
        "models": ["sonic-2", "sonic-english"],
        "voices": ["sonic-english", "british-lady", "helpful-woman"],
        "requires_key": "CARTESIA_API_KEY",
    },
    "elevenlabs": {
        "models": ["turbo-v2.5", "multilingual-v2"],
        "voices": ["rachel", "clyde", "domi"],
        "requires_key": "ELEVENLABS_API_KEY",
    },
    "openai": {
        "models": ["tts-1", "tts-1-hd"],
        "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        "requires_key": "OPENAI_API_KEY",
    },
    "azure": {
        "models": ["neural"],
        "voices": ["en-US-JennyNeural", "en-US-GuyNeural"],
        "requires_key": "AZURE_SPEECH_KEY",
    },
    "google": {
        "models": ["journey"],
        "voices": ["Journey", "Puck", "Charon", "Kore"],
        "requires_key": "GOOGLE_API_KEY",
    },
}


def validate_config(config: ModelConfig) -> bool:
    """Validate that the configuration is valid"""
    
    # Check if providers exist
    if config.stt_provider not in STT_PROVIDERS:
        raise ValueError(f"Invalid STT provider: {config.stt_provider}")
    
    if config.llm_provider not in LLM_PROVIDERS:
        raise ValueError(f"Invalid LLM provider: {config.llm_provider}")
    
    if config.tts_provider not in TTS_PROVIDERS:
        raise ValueError(f"Invalid TTS provider: {config.tts_provider}")
    
    # Check if required API keys are set
    stt_key = STT_PROVIDERS[config.stt_provider]["requires_key"]
    if not os.getenv(stt_key):
        raise ValueError(f"Missing required API key: {stt_key}")
    
    llm_key = LLM_PROVIDERS[config.llm_provider]["requires_key"]
    if not os.getenv(llm_key):
        raise ValueError(f"Missing required API key: {llm_key}")
    
    tts_key = TTS_PROVIDERS[config.tts_provider]["requires_key"]
    if not os.getenv(tts_key):
        raise ValueError(f"Missing required API key: {tts_key}")
    
    return True