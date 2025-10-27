import logging
import os
from datetime import datetime
from uuid import uuid4
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from memory.conversation_memory import ConversationMemory
from memory.storage import MemoryStorage
from models.context import AgentContext, ConversationContext, OrganizationContext, UserContext
from prompts.manager import PromptManager
from prompts.renderer import PromptRenderer

from telephony.inbound_handler import handle_inbound_call
from telephony.outbound_handler import make_outbound_call
from telephony.sip_config import is_sip_participant

from config.config import ModelConfig, validate_config

logger = logging.getLogger("voice-agent")
load_dotenv(".env")

prompt_manager = PromptManager()
prompt_renderer = PromptRenderer()
memory_storage = MemoryStorage()
conversation_memory = ConversationMemory(memory_storage)

# Load model configuration
model_config = ModelConfig.from_env()

# Validate configuration
try:
    validate_config(model_config)
    logger.info(f"Using STT: {model_config.stt_provider}/{model_config.stt_model}")
    logger.info(f"Using LLM: {model_config.llm_provider}/{model_config.llm_model}")
    logger.info(f"Using TTS: {model_config.tts_provider}/{model_config.tts_model}")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise


class VoiceAssistant(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)


def prewarm(proc: JobProcess):
    """Preload models for faster startup"""
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main entry point for the agent"""
    
    # Log context setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "stt": model_config.stt_provider,
        "llm": model_config.llm_provider,
        "tts": model_config.tts_provider,
    }

    await memory_storage.initialize()

    # Connect to room
    await ctx.connect()

    # Check if this is an outbound call from job metadata
    phone_number = None
    if ctx.job.metadata:
        phone_number = ctx.job.metadata.get("phone_number")

    # If outbound call, create SIP participant
    if phone_number:
        logger.info(f"Making outbound call to {phone_number}")
        await make_outbound_call(phone_number, ctx.room.name)


    # Wait for participant
    participant = await ctx.wait_for_participant()
    is_phone = is_sip_participant(participant)

    # Create user context
    user = UserContext(
        user_id=participant.identity or str(uuid4()),
        phone_number=phone_number if is_phone else None,
    )

    # Get or create user profile from memory
    user_context = await conversation_memory.get_user_context(user.user_id)
    if user_context and user_context.get("profile"):
        profile = user_context["profile"]
        user.name = profile.get("name")
        user.email = profile.get("email")

    # Create organization context (in production, load from database)
    organization = OrganizationContext(
        org_id="default",
        name=os.getenv("ORG_NAME", "Your Company"),
        industry=os.getenv("ORG_INDUSTRY"),
    )

    # Create conversation
    conversation = await conversation_memory.create_conversation(
        user, metadata={"is_phone": is_phone, "room": ctx.room.name}
    )

    # Build agent context
    agent_context = AgentContext(
        user=user,
        organization=organization,
        conversation=conversation,
        is_phone_call=is_phone,
        call_metadata={"participant_id": participant.identity},
    )

    # Select prompt based on context
    if is_phone:
        prompt = prompt_manager.get_prompt("phone_receptionist")
    else:
        prompt = prompt_manager.get_prompt("base_assistant")

    # Fallback to default if prompt not found
    if not prompt:
        logger.warning("Prompt not found, using default")
        instructions = """You are a helpful voice AI assistant. Keep responses concise and conversational."""
    else:
        # Render prompt with context
        instructions = prompt_renderer.render(prompt, agent_context)
        logger.info(f"Using prompt: {prompt.id}")
    
    logger.debug(f"Rendered instructions: {instructions}")


    # Set up voice AI session with configured models
    session = AgentSession(
        # Speech-to-text
        stt=model_config.get_stt_descriptor(),
        # Large Language Model
        llm=model_config.get_llm_descriptor(),
        # Text-to-speech with voice
        tts=f"{model_config.get_tts_descriptor()}:{model_config.tts_voice}",
        # Voice Activity Detection
        vad=ctx.proc.userdata.get("vad") or silero.VAD.load(),
        # Turn detection
        turn_detection=MultilingualModel(),
    )

    # Start the agent session
    await session.start(
        room=ctx.room,
        agent=VoiceAssistant(instructions=instructions),
        room_input_options=RoomInputOptions(
            # Enhanced noise cancellation
            noise_cancellation=noise_cancellation.BVCNoiseCancellation(),
        ),
    )

    logger.info("Voice agent started successfully")

    # Set up message logging
    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        logger.info(f"Track subscribed: {track.kind} from {participant.identity}")

    # Log all messages to memory
    conversation_id = conversation.conversation_id
    # Handle different greetings based on context
    if is_phone:
        caller_info = await handle_inbound_call(ctx, participant)
        greeting = f"Hello, thanks for calling {organization.name}. How can I help you today?"

        # Update user profile with phone number if we got it
        if caller_info.get("number") and caller_info["number"] != "Unknown":
            await conversation_memory.update_user_profile(
                user.user_id, {"phone_number": caller_info["number"]}
            )
    else:
        if user.name:
            greeting = f"Hello {user.name}! How can I help you today?"
        else:
            greeting = "Hello! How can I help you today?"

    # Generate greeting
    await session.generate_reply(instructions=f"Say: {greeting}")
    await log_message(conversation_id, "assistant", greeting)

    logger.info(f"Agent ready for conversation {conversation_id}")

async def log_message(conversation_id: str, role: str, content: str):
        """Log message to conversation memory"""
        await conversation_memory.add_message(conversation_id, role, content)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )