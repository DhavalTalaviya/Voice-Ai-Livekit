"""
Interactive model selector for easy configuration
"""
import os
from config.config import STT_PROVIDERS, LLM_PROVIDERS, TTS_PROVIDERS


def select_stt_provider():
    """Interactive STT provider selection"""
    print("\n=== Select STT Provider ===")
    providers = list(STT_PROVIDERS.keys())
    for i, provider in enumerate(providers, 1):
        print(f"{i}. {provider}")
    
    choice = int(input("\nEnter choice (1-{}): ".format(len(providers))))
    provider = providers[choice - 1]
    
    # Select model
    models = STT_PROVIDERS[provider]["models"]
    print(f"\n=== Select {provider} Model ===")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    model_choice = int(input("\nEnter choice (1-{}): ".format(len(models))))
    model = models[model_choice - 1]
    
    # Select language
    languages = STT_PROVIDERS[provider]["languages"]
    print(f"\n=== Select Language ===")
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang}")
    
    lang_choice = int(input("\nEnter choice (1-{}): ".format(len(languages))))
    language = languages[lang_choice - 1]
    
    return provider, model, language


def select_llm_provider():
    """Interactive LLM provider selection"""
    print("\n=== Select LLM Provider ===")
    providers = list(LLM_PROVIDERS.keys())
    for i, provider in enumerate(providers, 1):
        print(f"{i}. {provider}")
    
    choice = int(input("\nEnter choice (1-{}): ".format(len(providers))))
    provider = providers[choice - 1]
    
    # Select model
    models = LLM_PROVIDERS[provider]["models"]
    print(f"\n=== Select {provider} Model ===")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    model_choice = int(input("\nEnter choice (1-{}): ".format(len(models))))
    model = models[model_choice - 1]
    
    return provider, model


def select_tts_provider():
    """Interactive TTS provider selection"""
    print("\n=== Select TTS Provider ===")
    providers = list(TTS_PROVIDERS.keys())
    for i, provider in enumerate(providers, 1):
        print(f"{i}. {provider}")
    
    choice = int(input("\nEnter choice (1-{}): ".format(len(providers))))
    provider = providers[choice - 1]
    
    # Select model
    models = TTS_PROVIDERS[provider]["models"]
    print(f"\n=== Select {provider} Model ===")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    model_choice = int(input("\nEnter choice (1-{}): ".format(len(models))))
    model = models[model_choice - 1]
    
    # Select voice
    voices = TTS_PROVIDERS[provider]["voices"]
    print(f"\n=== Select Voice ===")
    for i, voice in enumerate(voices, 1):
        print(f"{i}. {voice}")
    
    voice_choice = int(input("\nEnter choice (1-{}): ".format(len(voices))))
    voice = voices[voice_choice - 1]
    
    return provider, model, voice


def update_env_file():
    """Interactive configuration updater"""
    print("=== Voice AI Model Configuration ===")
    
    # STT Selection
    stt_provider, stt_model, stt_language = select_stt_provider()
    
    # LLM Selection
    llm_provider, llm_model = select_llm_provider()
    
    # TTS Selection
    tts_provider, tts_model, tts_voice = select_tts_provider()
    
    # Generate .env content
    env_content = f"""# Generated Configuration
STT_PROVIDER={stt_provider}
STT_MODEL={stt_model}
STT_LANGUAGE={stt_language}

LLM_PROVIDER={llm_provider}
LLM_MODEL={llm_model}

TTS_PROVIDER={tts_provider}
TTS_MODEL={tts_model}
TTS_VOICE={tts_voice}

# Required API Keys
{STT_PROVIDERS[stt_provider]["requires_key"]}=your_key_here
{LLM_PROVIDERS[llm_provider]["requires_key"]}=your_key_here
{TTS_PROVIDERS[tts_provider]["requires_key"]}=your_key_here
"""
    
    print("\n=== Configuration Summary ===")
    print(f"STT: {stt_provider}/{stt_model} ({stt_language})")
    print(f"LLM: {llm_provider}/{llm_model}")
    print(f"TTS: {tts_provider}/{tts_model} (voice: {tts_voice})")
    print("\n" + env_content)
    
    save = input("\nSave to .env file? (y/n): ")
    if save.lower() == 'y':
        with open('.env', 'a') as f:
            f.write(env_content)
        print("Configuration saved to .env")
    else:
        print("Configuration not saved")


if __name__ == "__main__":
    update_env_file()