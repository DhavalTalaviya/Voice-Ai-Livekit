"""Script to make outbound phone calls"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from livekit import api

load_dotenv()


async def make_call(phone_number: str):
    """
    Dispatch agent and make outbound call
    
    Args:
        phone_number: Phone number to call (format: +1234567890)
    """
    
    livekit_api = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )
    
    try:
        # Create unique room name
        room_name = f"call-{phone_number.replace('+', '')}"
        
        print(f"\n Making outbound call...")
        print(f"   Phone: {phone_number}")
        print(f"   Room: {room_name}")
        
        # Dispatch the agent with phone number in metadata
        dispatch = await livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name="my-voice-agent",
                room=room_name,
                metadata={"phone_number": phone_number},
            )
        )
        
        print(f"\nAgent dispatched successfully!")
        print(f"   Dispatch ID: {dispatch.id}")
        print(f"   Agent will call {phone_number} shortly...")
        
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)
    finally:
        await livekit_api.aclose()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/make_call.py +1234567890")
        print("\nExample:")
        print("  python scripts/make_call.py +12025551234")
        sys.exit(1)
    
    phone_number = sys.argv[1]
    
    # Validate phone number format
    if not phone_number.startswith("+"):
        print("Error: Phone number must start with + (e.g., +1234567890)")
        sys.exit(1)
    
    asyncio.run(make_call(phone_number))