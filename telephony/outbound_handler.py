import logging
import os
from livekit import api

logger = logging.getLogger("outbound-handler")


async def make_outbound_call(phone_number: str, room_name: str):
    """
    Make an outbound phone call
    
    Args:
        phone_number: Phone number to call (e.g., +1234567890)
        room_name: LiveKit room name for the call
        
    Returns:
        SIP participant object
    """
    
    livekit_url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    sip_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    if not sip_trunk_id:
        logger.error("SIP_OUTBOUND_TRUNK_ID not set")
        raise ValueError("SIP_OUTBOUND_TRUNK_ID is required for outbound calls")
    
    logger.info(f"Initiating outbound call to {phone_number}")

    # Create LiveKit API client
    livekit_api = api.LiveKitAPI(livekit_url, api_key, api_secret)
    
    try:
        # Create SIP participant
        sip_participant = await livekit_api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                sip_trunk_id=sip_trunk_id,
                sip_call_to=phone_number,
                room_name=room_name,
                participant_identity=f"sip_{phone_number.replace('+', '')}",
                participant_name=f"Call to {phone_number}",
            )
        )
        
        logger.info(f"Outbound call created successfully")
        logger.info(f"SIP Participant ID: {sip_participant.sip_participant_id}")  
        return sip_participant
        
    except Exception as e:
        logger.error(f"Failed to create outbound call: {e}")
        raise
    finally:
        await livekit_api.aclose()