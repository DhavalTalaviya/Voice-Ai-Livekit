import logging
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import silero

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant. Keep responses brief."
        )


async def entrypoint(ctx: JobContext):
    logger.info("Starting agent")
    await ctx.connect()
    
    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-2:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
    )
    
    await session.start(room=ctx.room, agent=Assistant())
    await session.generate_reply(instructions="Say hello")
    
    logger.info("Agent started")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint
        )
    )